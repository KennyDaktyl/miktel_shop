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

from .forms import LoginForm, UserForm, BusinessForm
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
                user = User.objects.get(email=form.cleaned_data['email'])
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
                user = User.objects.get(email=form.cleaned_data['email'])
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
                address.user_id = new_user
                address.street = form.cleaned_data['street']
                address.house = form.cleaned_data['house']
                if form.cleaned_data['door']:
                    address.door = form.cleaned_data['door']
                address.zip_code = form.cleaned_data['zip_code']
                address.city = form.cleaned_data['city']
                address.save()
                login(request, new_user)
                messages.error(request, 'Utworzono konto')
                return redirect('front_page')
        else:
            messages.error(request, 'Wystąpił błąd')
            ctx = {'form': form}
            return render(request, "accounts/register_business.html", ctx)


class Activate(View):

    def get_user_agent(self):
        return self.request.META.get("HTTP_USER_AGENT", "")

    def get_ip(self):
        return self.request.META.get("REMOTE_ADDR", "")

    def post(self, request, *args, **kwargs):
        # ser = ActivateSerializer(data=request.data)
        # ser.is_valid(raise_exception=True)
        # vd = ser.validated_data
        try:
            u = User.objects.get(activation_token=vd['token'])
        except User.DoesNotExist:
            raise ValidationError("bad activation", "bad_activation")

        # if u.activation_send_time and (timezone.now() - u.activation_send_time) > \
        #         timedelta(minutes=settings.ACTIVATION_EXPIRATION_MINUTES):
        #     raise ValidationError(code='activation_expired',
        #                           detail='Email activation token expired.')

        u.activation_token = None
        u.activation_send_time = None
        u.is_active = True  # Not anymore.
        u.is_email_confirmed = True
        u.save()
            
        send_account_activated_email(to=u.email, recipient=u)
        data = ActivateUserInfoOutSerializer(u).data

        return Response(data_out.data)

# # @method_decorator(login_required, name='dispatch')
# # class ChangeOnlyPasswordView(View):
# #     permission_required = 'account.add_profile'

# #     def get(self, request, pk):
# #         profile = Profile.objects.get(pk=pk)
# #         form_pswd = PasswordChangeForm()
# #         ctx = {'form_pswd': form_pswd, 'profile': profile}
# #         return render(request, "account/change_only_password.html", ctx)

# #     def post(self, request, pk):
# #         form_pswd = PasswordChangeForm(request.POST)
# #         profile = Profile.objects.get(pk=pk)
# #         user = User.objects.get(pk=profile.user.id)
# #         if form_pswd.is_valid():
# #             user.set_password(form_pswd.cleaned_data['password'])
# #             user.save()
# #             messages.error(request, 'Hasło zostało zmienione')
# #             return redirect('profile_list')
# #         else:
# #             messages.error(request, 'Wystąpił błąd')
# #             ctx = {'form_pswd': form_pswd, 'profile': profile}
# #             return render(request, "account/change_only_password.html", ctx)

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
            user = authenticate(request, username=user_name_email, password=password)
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
company_registration = CompanyRegistrationView.as_view()