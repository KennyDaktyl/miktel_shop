import re
from datetime import datetime

from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from django import forms

# from .models import Profile, Address
# from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

User = get_user_model()

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


class LoginForm(forms.Form):
    # username = forms.CharField(label="Login", required=True)

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput,
        validators=[validate_email],
        required=True,
    )
    password = forms.CharField(
        label="Hasło", widget=forms.PasswordInput, required=True
    )


class UserForm(forms.ModelForm):
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput,
        validators=[validate_email],
        required=True,
    )
    # first_name = forms.CharField(label="Imię", required=True)
    # last_name = forms.CharField(label="Nazwisko", required=True)

    # phone_number = forms.CharField(label="Telefon", required=True)

    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput,
        min_length=6,
        help_text="Minimum 6 znaków",
        required=True,
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        widget=forms.PasswordInput,
        min_length=6,
        required=True,
    )

    # email = forms.EmailField(label="email",
    #                          widget=forms.EmailInput,
    #                          validators=[validate_email],
    #                          required=True)
    # street = forms.CharField(label="Ulica", max_length=128, required=True)
    # house = forms.CharField(label="Nr domu", max_length=8, required=True)
    # door = forms.CharField(label="Nr lokalu", max_length=8, required=False)
    # city = forms.CharField(label="Miasto", max_length=64, required=True)
    # zip_code = forms.CharField(label="Kod pocztowy",min_length=6, max_length=6, required=True)
    # captcha = ReCaptchaField(required=True)

    # is_active = forms.BooleanField(
    #     help_text="Czy użytkownik jest aktywny? (Odznacz zamiast kasować)")

    class Meta:
        model = User
        fields = (
            # 'username',
            "email",
            # 'first_name',
            # 'last_name',
            "password",
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Hasła nie są identyczne.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Zły format email.")

        return email


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput,
        min_length=6,
        help_text="Minimum 6 znaków",
        required=True,
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        widget=forms.PasswordInput,
        min_length=6,
        required=True,
    )

    class Meta:
        model = User
        fields = ("password",)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Hasła nie są identyczne.")
        return cd["password2"]


class BusinessForm(forms.ModelForm):
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput,
        validators=[validate_email],
        required=True,
    )
    business_name = forms.CharField(
        label="Nazwa firmy", max_length=128, required=True
    )
    business_name_l = forms.CharField(
        label="nazwa c.d.", max_length=128, required=False
    )
    nip_number = forms.CharField(
        label="NIP",
        required=True,
        min_length=10,
        max_length=10,
    )
    phone_number = forms.CharField(
        label="Telefon",
        required=True,
        min_length=6,
        max_length=15,
    )

    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput,
        min_length=6,
        help_text="Minimum 6 znaków",
        required=True,
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        widget=forms.PasswordInput,
        min_length=6,
        required=True,
    )
    street = forms.CharField(label="Ulica", max_length=128, required=True)
    house = forms.CharField(label="Nr domu", max_length=8, required=True)
    door = forms.CharField(label="Nr lokalu", max_length=8, required=False)
    city = forms.CharField(label="Miasto", max_length=64, required=True)
    zip_code = forms.CharField(
        label="Kod pocztowy", max_length=6, required=True
    )
    # captcha = ReCaptchaField(required=True)

    # is_active = forms.BooleanField(
    #     help_text="Czy użytkownik jest aktywny? (Odznacz zamiast kasować)")

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Hasła nie są identyczne.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Zły format email.")

        return email

        return cd["password2"]


class AddressForm(forms.Form):
    street = forms.CharField(label="Ulica", max_length=128, required=True)
    house = forms.CharField(label="Nr domu", max_length=8, required=True)
    door = forms.CharField(label="Nr lokalu", max_length=8, required=False)
    city = forms.CharField(label="Miasto", max_length=64, required=True)
    zip_code = forms.CharField(
        label="Kod pocztowy", max_length=6, required=True
    )


# class PasswordChangeForm(forms.Form):
#     password = forms.CharField(label="Hasło",
#                                widget=forms.PasswordInput,
#                                min_length=6,
#                                help_text="Minimum 6 znaków",
#                                required=True)
#     password2 = forms.CharField(label="Powtórz hasło",
#                                 widget=forms.PasswordInput,
#                                 min_length=6,
#                                 required=True)

#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Hasła nie są identyczne.')
#         return cd['password2']


# # class UserProfileForm(forms.ModelForm):
# #     class Meta:
# #         model = User
# #         fields = ('username', 'first_name', 'last_name', 'email')


# class AddressBasketForm(forms.ModelForm):
#     class Meta:
#         model = Address
#         exclude = ('user_id', )
