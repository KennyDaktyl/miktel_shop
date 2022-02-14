from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from django import forms


class ContactForm(forms.Form):
    helper = FormHelper()
    name = forms.CharField(
        label="Imie i nazwisko",
        widget=forms.TextInput(attrs={"placeholder": "Full name"}),
        required=True,
    )
    email = forms.EmailField(
        label="Podaj swój email kontaktowy",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
        required=True,
    )
    subject = forms.CharField(
        label="Temat wiadomości",
        widget=forms.TextInput(attrs={"placeholder": "Subject"}),
        required=True,
    )
    message = forms.CharField(
        label="Treść wiadomości",
        widget=forms.Textarea(
            attrs={"cols": 30, "rows": 4, "placeholder": "message"}
        ),
        required=True,
    )

    captcha = ReCaptchaField(required=True)
