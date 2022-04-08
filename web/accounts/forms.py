import re
from django import forms

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from web.models.accounts import Profile

User = get_user_model()

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


def is_digit(value):
    value = value.replace(" ", "")
    value = value.replace("-", "")
    if value.isdigit() is False:
        raise ValidationError("Wpisuj tylko cyfry")


class LoginForm(forms.Form):

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput,
        validators=[validate_email],
        required=True,
    )
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput, required=True)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Zły format email.")
        return email


class UserForm(forms.ModelForm):
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput,
        validators=[validate_email],
        required=True,
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

    class Meta:
        model = User
        fields = (
            "email",
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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Zły format email.")
        return email


class StandartForm(forms.ModelForm):

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput,
        validators=[validate_email],
        required=True,
    )

    phone_number = forms.CharField(
        label="Telefon",
        required=False,
        min_length=6,
        max_length=15,
        validators=[is_digit],
    )

    class Meta:
        model = Profile
        fields = ("phone_number",)

    def only_int(value):
        if value.isdigit() is False:
            raise ValidationError("Wpisuj tylko cyfry")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Zły format email.")
        return email


class BusinessForm(forms.ModelForm):

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput,
        validators=[validate_email],
        required=True,
    )
    business_name = forms.CharField(label="Nazwa firmy", max_length=128, required=True)
    business_name_l = forms.CharField(
        label="nazwa c.d.", max_length=128, required=False
    )
    nip_number = forms.CharField(
        label="NIP",
        required=True,
        min_length=10,
        max_length=16,
        validators=[is_digit],
    )
    phone_number = forms.CharField(
        label="Telefon",
        required=True,
        min_length=6,
        max_length=15,
        validators=[is_digit],
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
    zip_code = forms.CharField(label="Kod pocztowy", max_length=6, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Zły format email.")
        else:
            return email


class CompanyForm(forms.ModelForm):

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput,
        validators=[validate_email],
        required=True,
    )
    phone_number = forms.CharField(
        label="Telefon",
        required=True,
        min_length=6,
        max_length=15,
        validators=[is_digit],
    )
    nip_number = forms.CharField(
        label="NIP",
        required=True,
        min_length=10,
        max_length=10,
        validators=[is_digit],
    )

    class Meta:
        model = Profile
        fields = (
            "email",
            "company_name",
            "company_name_l",
            "nip_number",
            "phone_number",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Zły format email.")
        else:
            return email

    def only_int(self):
        nip_number = self.cleaned_data.get("nip_number")
        phone_number = self.cleaned_data.get("phone_number")
        if nip_number.isdigit() is False or phone_number.isdigit() is False:
            raise ValidationError("Wpisuj tylko cyfry")


class AddressForm(forms.Form):
    street = forms.CharField(label="Ulica", max_length=128, required=True)
    house = forms.CharField(label="Nr domu", max_length=8, required=True)
    door = forms.CharField(label="Nr lokalu", max_length=8, required=False)
    city = forms.CharField(label="Miasto", max_length=64, required=True)
    zip_code = forms.CharField(label="Kod pocztowy", max_length=6, required=True)
