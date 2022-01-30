from audioop import add
import uuid
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.views import LogoutView

from django.views import View
# from django.views.generic.edit \
#     import CreateView, UpdateView, DeleteView
from django.contrib import messages
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
# from django.urls import reverse_lazy, reverse
# from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from web.models.accounts import ActivateToken
from web.models.orders import Orders

from .forms import LoginForm, UserForm, BusinessForm, ChangePasswordForm, AddressForm
from .functions import *
# from products.models import Category
from web.models import Profile, Address

User = get_user_model()


# class ChoiceAccountReqisterView(View):
#     def get(self, request):
#         categorys = Category.objects.filter(is_active=True)
#         form = LoginForm()
#         ctx = {'form': form, 'categorys': categorys}
#         return render(request, "account/choice_account_register.html", ctx)

#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 # token = Token.objects.get_or_create(user=user)
#                 login(request, user)
#                 return redirect('order_details')
#             else:
#                 messages.error(request, 'Błędne hasło lub login')
#                 ctx = {'form': form}
#                 return render(request, "account/choice_account_register.html",
#                               ctx)
#         else:
#             messages.error(request, 'Błędne hasło lub login')
#             ctx = {'form': form}
#             return render(request, "account/choice_account_register.html", ctx)


class RegisterUserView(View):
    def get(self, request):
        form = UserForm()
        ctx = {'form': form}
        return render(request, "accounts/register_user.html", ctx)

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['email'])
                messages.error(request, 'Email już istnieje w naszej bazie.')
                ctx = {'form': form}
                return render(request, "accounts/register_user.html", ctx)
            except User.DoesNotExist:
                new_user = form.save(commit=False)
                new_user.username = form.cleaned_data['email']
                new_user.email = form.cleaned_data['email']
                new_user.set_password(form.cleaned_data['password'])
                new_user.is_active = False
                new_user.save()
                host = request.scheme + "://" + request.get_host()
                token = ActivateToken.objects.create(
                    user=new_user, activation_token=str(int(str(uuid.uuid4()).split('-')[0], 16)))
                send_simple_message('Aktywacja konta', host,
                                    new_user, token.activation_token)
                profile = Profile()
                profile.user_id = new_user.id
                profile.company = False
                profile.save()
                messages.error(request, 'Potwierdź email aby zalogować.')
                return redirect('front_page')
        else:
            messages.error(request, 'Wystąpił błąd')
            ctx = {'form': form}
            return render(request, "accounts/register_user.html", ctx)


class CompanyRegistrationView(View):
    def get(self, request):
        form = BusinessForm()
        ctx = {'form': form}
        return render(request, "accounts/register_business.html", ctx)

    def post(self, request):
        form = BusinessForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['email'])
                messages.error(request, 'Email już istnieje w naszej bazie.')
                ctx = {'form': form}
                return render(request, "accounts/register_user.html", ctx)
            except User.DoesNotExist:
                new_user = form.save(commit=False)
                new_user.username = form.cleaned_data['email']
                new_user.email = form.cleaned_data['email']
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()

                profile = Profile()
                profile.user_id = new_user.id
                profile.business_name = form.cleaned_data['business_name']
                profile.business_name_l = form.cleaned_data['business_name_l']
                profile.phone_number = form.cleaned_data['phone_number']
                profile.nip_number = form.cleaned_data['nip_number']
                profile.company = True
                profile.save()

                address = Address()
                address.user_id = new_user.id
                address.street = form.cleaned_data['street']
                address.house = form.cleaned_data['house']
                if form.cleaned_data['door']:
                    address.door = form.cleaned_data['door']
                address.zip_code = form.cleaned_data['zip_code']
                address.city = form.cleaned_data['city']
                address.save()
                host = request.scheme + "://" + request.get_host()
                token = ActivateToken.objects.create(
                    user=new_user, activation_token=str(int(str(uuid.uuid4()).split('-')[0], 16)))
                send_simple_message('Aktywacja konta', host,
                                    new_user, token.activation_token)
                messages.error(request, 'Potwierdź email aby zalogować.')
                return redirect('front_page')
        else:
            messages.error(request, 'Wystąpił błąd')
            print(form.errors)
            ctx = {'form': form}
            return render(request, "accounts/register_business.html", ctx)


class ActivateAccount(View):

    def get(self, request, token):
        user = ActivateToken.objects.get(activation_token=token).user
        user.is_active = True
        user.save()
        messages.error(request, 'Konto aktywne.')
        login(request, user)
        return redirect('front_page')


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
class UserProfile(View):

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        ctx = {"profile": profile}
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
                "city": address.city
            })
        ctx = {'address_form': address_form, 'user_address': address}
        return render(request, "accounts/user_account.html", ctx)

    def post(self, request):
        address_form = AddressForm(request.POST)
        address = Address.objects.filter(user=request.user).first()
        if address_form.is_valid():
            if not address:
                address = Address()
                address.user= request.user
            address.street = address_form.cleaned_data['street']
            address.house = address_form.cleaned_data['house']
            address.post_code = address_form.cleaned_data['zip_code']
            address.city = address_form.cleaned_data['city']
            if address_form.cleaned_data['door']:
                address.door = address_form.cleaned_data['door']
            address.save()
            messages.error(request, 'Zapisano nowy adres.')
            return render(request, "accounts/user_account.html")

        else:
            messages.error(request, 'Wystąpił błąd')
            ctx = {'addres_form': address_form}
            return render(request, "accounts/register_business.html", ctx)


# class Activate(View):

#     def get_user_agent(self):
#         return self.request.META.get("HTTP_USER_AGENT", "")

#     def get_ip(self):
#         return self.request.META.get("REMOTE_ADDR", "")

#     def post(self, request, *args, **kwargs):
#         # ser = ActivateSerializer(data=request.data)
#         # ser.is_valid(raise_exception=True)
#         # vd = ser.validated_data
#         try:
#             u = User.objects.get(activation_token=vd['token'])
#         except User.DoesNotExist:
#             raise ValidationError("bad activation", "bad_activation")

#         # if u.activation_send_time and (timezone.now() - u.activation_send_time) > \
#         #         timedelta(minutes=settings.ACTIVATION_EXPIRATION_MINUTES):
#         #     raise ValidationError(code='activation_expired',
#         #                           detail='Email activation token expired.')

#         u.activation_token = None
#         u.activation_send_time = None
#         u.is_active = True  # Not anymore.
#         u.is_email_confirmed = True
#         u.save()

#         send_account_activated_email(to=u.email, recipient=u)
#         data = ActivateUserInfoOutSerializer(u).data

#         return Response(data_out.data)

@method_decorator(login_required, name='dispatch')
class ChangeOnlyPasswordView(View):

    def get(self, request):
        form = ChangePasswordForm()
        ctx = {'form': form}
        return render(request, "accounts/user_account.html", ctx)

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            messages.error(request, 'Hasło zostało zmienione')
            return render(request, "accounts/user_account.html")
        else:
            messages.error(request, 'Wystąpił błąd')
            ctx = {'form': form}
            return render(request, "accounts/user_account.html", ctx)

# # @method_decorator(login_required, name="dispatch")
# # class UpdateUserView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
# #     permission_required = "account.change_user"
# #     model = User
# #     # fields = "__all__"
# #     form_class = UserProfileForm
# #     template_name_suffix = "_update_form"
# #     success_url = reverse_lazy("profile_list")
# #     success_message = 'Zaktualizowano konto użytkownika'

# # @method_decorator(login_required, name="dispatch")
# # class UpdateProfileView(PermissionRequiredMixin, SuccessMessageMixin,
# #                         UpdateView):
# #     permission_required = "account.change_profile"
# #     model = Profile
# #     # fields = "__all__"
# #     form_class = ProfileForm
# #     template_name_suffix = "_update_form"
# #     success_url = reverse_lazy("profile_list")
# #     success_message = 'Zaktualizowano profil użytkownika'

# #     # def form_valid(self, form):
# #     #     form.instance.user = SubCategory.objects.get(
# #     #         pk=self.kwargs.get('pk'))
# #     #     return super().form_valid(form)

# # @method_decorator(login_required, name="dispatch")
# # class DeleteProfileView(PermissionRequiredMixin, SuccessMessageMixin,
# #                         DeleteView):
# #     permission_required = "account.delete_profile"
# #     model = Profile
# #     fields = "__all__"
# #     template_name_suffix = "_confirm_delete"
# #     success_url = reverse_lazy("profile_list")
# #     success_message = 'Usunięto konto'

# #     def delete(self, request, *args, **kwargs):
# #         messages.success(self.request, self.success_message)
# #         return super(DeleteProfileView, self).delete(request, *args, **kwargs)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {'form': form}
        return render(request, "accounts/login.html", ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name_email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(
                request, username=user_name_email, password=password)
            if user is not None:
                # token = Token.objects.get_or_create(user=user)
                login(request, user)
                messages.error(request, 'Zalogowano poprawnie.')
                return redirect('front_page')
            else:
                messages.error(request, 'Błędne hasło lub login')
                ctx = {'form': form}
                return render(request, "accounts/login.html", ctx)
        else:
            messages.error(request, 'Błędne hasło lub login')
            ctx = {'form': form}
            return render(request, "accounts/login.html", ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.error(request, 'Wylogowano poprawnie.')
        return redirect('login')


# @method_decorator(login_required, name='dispatch')
# class AddAddressBasketView(SuccessMessageMixin, CreateView):

#     model = Address
#     form_class = AddressBasketForm

#     success_message = 'Dodano adres klienta'
#     success_url = ("")

#     def get_initial(self, *args, **kwargs):
#         initial = super(AddAddressBasketView, self).get_initial(**kwargs)
#         initial['user'] = self.request.user
#         return initial

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user_id = self.request.user
#         self.object.save()
#         print(form.instance.user_id, )
#         return HttpResponseRedirect(self.get_success_url())

#     def get_success_url(self, *args, **kwargs):
#         return reverse('order_details')


# @method_decorator(login_required, name='dispatch')
# class UpdateAddressBasketView(SuccessMessageMixin, UpdateView):

#     model = Address
#     form_class = AddressBasketForm
#     template_name_suffix = "_update_form"
#     success_message = 'Dodano adres klienta'
#     success_url = ("")

#     def get_initial(self, *args, **kwargs):
#         initial = super(UpdateAddressBasketView, self).get_initial(**kwargs)
#         initial['user'] = self.request.user
#         return initial

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user_id = self.request.user
#         self.object.main = True
#         self.object.save()
#         print(form.instance.user_id, )
#         return HttpResponseRedirect(self.get_success_url())

#     def get_success_url(self, *args, **kwargs):
#         return reverse('order_details')


# @method_decorator(login_required, name="dispatch")
# class DeleteAddressBasketView(SuccessMessageMixin, DeleteView):
#     model = Address
#     fields = "__all__"
#     template_name_suffix = "_confirm_delete"
#     success_url = reverse_lazy("order_details")
#     success_message = 'Usunięto adres'

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super(DeleteAddressBasketView,
#                      self).delete(request, *args, **kwargs)


user_login = LoginView.as_view()
user_logout = LogoutView.as_view()
register_user = RegisterUserView.as_view()
activate_account = ActivateAccount.as_view()
company_registration = CompanyRegistrationView.as_view()
user_account = UserAccount.as_view()
user_orders = UserOrders.as_view()
change_password = ChangeOnlyPasswordView.as_view()
user_addresses = UserAddress.as_view()
user_profile = UserProfile.as_view()
