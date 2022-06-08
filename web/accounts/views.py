from uuid import uuid4

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from web.models import Address, Profile
from web.models.accounts import ActivateToken
from web.models.orders import Orders

from .forms import (
    AddressForm,
    BusinessForm,
    ChangePasswordForm,
    CompanyForm,
    LoginForm,
    StandartForm,
    UserForm,
)
from .functions import (
    send_simple_message,
    send_activate_info_message,
    send_activate_email_by_django,
    send_activate_info_email_by_django,
)

User = get_user_model()


class RegisterUserView(View):
    def get(self, request):
        form = UserForm()
        ctx = {"form": form}
        return render(request, "accounts/register_user.html", ctx)

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(username=form.cleaned_data["email"])
                messages.error(request, "Email już istnieje w naszej bazie.")
                ctx = {"form": form}
                return render(request, "accounts/register_user.html", ctx)
            except User.DoesNotExist:
                new_user = form.save(commit=False)
                new_user.username = form.cleaned_data["email"]
                new_user.email = form.cleaned_data["email"]
                new_user.set_password(form.cleaned_data["password"])
                new_user.is_active = False
                new_user.save()
                host = request.scheme + "://" + request.get_host()
                token = ActivateToken.objects.create(
                    user=new_user,
                    activation_token=str(int(str(uuid4()).split("-")[0], 16)),
                )
                # send_simple_message(
                #     "Aktywacja konta", host, new_user, token.activation_token
                # )
                send_activate_email_by_django(
                    "Aktywacja konta", host, new_user, token.activation_token)
                profile = Profile()
                profile.user_id = new_user.id
                profile.company = False
                profile.save()
                messages.error(
                    request, "Potwierdź email aby zalogować. (*Sprawdź Spam lub ofery)"
                )
                return redirect("front_page")
        else:
            messages.error(request, "Wystąpił błąd")
            ctx = {"form": form}
            return render(request, "accounts/register_user.html", ctx)


class CompanyRegistrationView(View):
    def get(self, request):
        form = BusinessForm()
        ctx = {"form": form}
        return render(request, "accounts/register_business.html", ctx)

    def post(self, request):
        form = BusinessForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(username=form.cleaned_data["email"])
                messages.error(request, "Email już istnieje w naszej bazie.")
                ctx = {"form": form}
                return render(request, "accounts/register_user.html", ctx)
            except User.DoesNotExist:
                new_user = form.save(commit=False)
                new_user.username = form.cleaned_data["email"]
                new_user.email = form.cleaned_data["email"]
                new_user.set_password(form.cleaned_data["password"])
                new_user.is_active = False
                new_user.save()

                profile = Profile()
                profile.user_id = new_user.id
                profile.company_name = form.cleaned_data["business_name"]
                profile.company_name_l = form.cleaned_data["business_name_l"]
                profile.phone_number = form.cleaned_data["phone_number"].replace(
                    " ", ""
                )
                profile.nip_number = form.cleaned_data["nip_number"]
                profile.company = True
                profile.save()

                address = Address()
                address.user_id = new_user.id
                address.street = form.cleaned_data["street"]
                address.house = form.cleaned_data["house"]
                if form.cleaned_data["door"]:
                    address.door = form.cleaned_data["door"]
                address.post_code = form.cleaned_data["zip_code"]
                address.city = form.cleaned_data["city"]
                address.save()
                host = request.scheme + "://" + request.get_host()
                token = ActivateToken.objects.create(
                    user=new_user,
                    activation_token=str(int(str(uuid4()).split("-")[0], 16)),
                )
                # send_simple_message(
                #     "Aktywacja konta", host, new_user, token.activation_token
                # )
                send_activate_email_by_django(
                    "Aktywacja konta", host, new_user, token.activation_token)
                messages.error(
                    request, "Potwierdź email aby zalogować. (*Sprawdź Spam lub ofery)"
                )
                return redirect("front_page")
        else:
            messages.error(request, "Wystąpił błąd")
            ctx = {"form": form}
            return render(request, "accounts/register_business.html", ctx)


class ActivateAccount(View):
    def get(self, request, token):
        user = ActivateToken.objects.get(activation_token=token).user
        user.is_active = True
        user.save()
        messages.error(request, "Konto aktywne.")
        login(request, user)
        send_activate_info_message(user)
        # send_activate_info_email_by_django(user)
        return redirect("front_page")


@method_decorator(login_required, name="dispatch")
class UserAccount(View):
    def get(self, request):
        ctx = {}
        return render(request, "accounts/user_account.html", ctx)


@method_decorator(login_required, name="dispatch")
class UserOrders(View):
    def get(self, request):
        orders = Orders.objects.filter(client=request.user)
        ctx = {"orders": orders}
        return render(request, "accounts/user_account.html", ctx)


@method_decorator(login_required, name="dispatch")
class UserProfileView(View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        if profile.company or request.GET.get("change_account"):
            bussines_form = CompanyForm(
                instance=profile, initial={"email": profile.user.email}
            )
            ctx = {
                "profile": profile,
                "bussines_form": bussines_form,
                "change_account": True,
            }
            return render(request, "accounts/user_account.html", ctx)
        else:
            standart_form = StandartForm(
                initial={
                    "email": profile.user.email,
                    "phone_number": profile.phone_number,
                }
            )
            ctx = {"profile": profile, "standart_form": standart_form}
            return render(request, "accounts/user_account.html", ctx)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        bussines_form = CompanyForm(request.POST)
        standart_form = StandartForm(request.POST)
        if "bussines_form" in request.POST:
            if bussines_form.is_valid():
                user = User.objects.get(profile=profile)
                user.email = bussines_form.cleaned_data["email"]
                user.save()
                bussines_form.save(commit=False)
                profile.company = True
                profile.company_name = bussines_form.cleaned_data["company_name"]
                profile.company_name_l = bussines_form.cleaned_data["company_name_l"]
                profile.nip_number = bussines_form.cleaned_data["nip_number"]
                profile.phone_number = bussines_form.cleaned_data["phone_number"]
                profile.save()
                messages.error(request, "Zapisano nowe dane.")
                return redirect("user_profile")
            else:
                profile = Profile.objects.get(user=request.user)
                bussines_form = CompanyForm(
                    request.POST,
                    initial={
                        "email": profile.user.email,
                        "company_name": profile.company_name,
                        "company_name_l": profile.company_name_l,
                        "nip_number": profile.nip_number,
                        "phone_number": profile.phone_number,
                    },
                )
                messages.error(request, "Błąd danych formularza")
                ctx = {
                    "profile": profile,
                    "bussines_form": bussines_form,
                    "change_account": True,
                }
                return render(request, "accounts/user_account.html", ctx)
        if "standart_form" in request.POST:
            if standart_form.is_valid():
                user = User.objects.get(profile=profile)
                user.email = standart_form.cleaned_data["email"]
                user.save()
                profile.phone_number = standart_form.cleaned_data["phone_number"]
                profile.save()
                messages.error(request, "Zapisano nowe dane.")
                return redirect("user_profile")
            else:
                standart_form = StandartForm(
                    request.POST,
                    initial={
                        "email": profile.user.email,
                        "phone_number": profile.phone_number,
                    },
                )
                messages.error(request, "Błąd danych formularza")
                ctx = {"profile": profile, "standart_form": standart_form}
                return render(request, "accounts/user_account.html", ctx)


@method_decorator(login_required, name="dispatch")
class UserAddress(View):
    def get(self, request):
        address = Address.objects.filter(user=request.user).first()
        if not address:
            address = "Brak dodanego adresu"
            ctx = {"address": address}
            return render(request, "accounts/user_account.html", ctx)
        address_form = AddressForm(
            initial={
                "street": address.street,
                "house": address.house,
                "door": address.door,
                "zip_code": address.post_code,
                "city": address.city,
            }
        )
        ctx = {"address_form": address_form, "user_address": address}
        return render(request, "accounts/user_account.html", ctx)

    def post(self, request):
        address_form = AddressForm(request.POST)
        address = Address.objects.filter(user=request.user).first()
        if address_form.is_valid():
            if not address:
                address = Address()
                address.user = request.user
            address.street = address_form.cleaned_data["street"]
            address.house = address_form.cleaned_data["house"]
            address.door = address_form.cleaned_data["door"]
            address.post_code = address_form.cleaned_data["zip_code"]
            address.city = address_form.cleaned_data["city"]
            address.save()
            messages.error(request, "Zapisano nowy adres.")
            return render(request, "accounts/user_account.html")

        else:
            messages.error(request, "Wystąpił błąd")
            ctx = {"addres_form": address_form}
            return render(request, "accounts/register_business.html", ctx)


@method_decorator(login_required, name="dispatch")
class ChangeOnlyPasswordView(View):
    def get(self, request):
        form = ChangePasswordForm()
        ctx = {"form": form}
        return render(request, "accounts/user_account.html", ctx)

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["password"])
            request.user.save()
            messages.error(request, "Hasło zostało zmienione")
            return render(request, "accounts/user_account.html")
        else:
            messages.error(request, "Wystąpił błąd")
            ctx = {"form": form}
            return render(request, "accounts/user_account.html", ctx)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {"form": form}
        return render(request, "accounts/login.html", ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name_email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=user_name_email, password=password)
            if user is not None:
                login(request, user)
                messages.error(request, "Zalogowano poprawnie.")
                return redirect("front_page")
            else:
                messages.error(request, "Błędne hasło lub login")
                ctx = {"form": form}
                return render(request, "accounts/login.html", ctx)
        else:
            messages.error(request, "Błędne hasło lub login")
            ctx = {"form": form}
            return render(request, "accounts/login.html", ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.error(request, "Wylogowano poprawnie.")
        return redirect("login")


user_login = LoginView.as_view()
user_logout = LogoutView.as_view()
register_user = RegisterUserView.as_view()
activate_account = ActivateAccount.as_view()
company_registration = CompanyRegistrationView.as_view()
user_account = UserAccount.as_view()
user_orders = UserOrders.as_view()
change_password = ChangeOnlyPasswordView.as_view()
user_addresses = UserAddress.as_view()
user_profile = UserProfileView.as_view()
