from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from django import forms
from web.models.orders import DeliveryMethod, PayMethod


class ContactForm(forms.Form):
    helper = FormHelper()
    email = forms.EmailField(
        label="Podaj swój email kontaktowy",
        widget=forms.EmailInput(attrs={"placeholder": "kowalski.janusz@gmail.com"}),
        required=True,
    )
    subject = forms.CharField(
        label="Temat wiadomości",
        widget=forms.TextInput(attrs={"placeholder": ""}),
        required=True,
    )
    message = forms.CharField(
        label="Treść wiadomości",
        widget=forms.Textarea(attrs={"size": 80, "cols": 30}),
        required=True,
    )

    captcha = ReCaptchaField(required=True)


class OrderBigForm(forms.Form):
    account = forms.CharField(
        label="Konto",
        max_length=64,
        required=True,
        widget=forms.HiddenInput(),
    )
    bill = forms.CharField(
        label="Dokument",
        max_length=64,
        required=True,
        widget=forms.HiddenInput(),
    )
    delivery = forms.CharField(
        label="Dostawa",
        max_length=64,
        required=True,
        widget=forms.HiddenInput(),
    )
    payment = forms.CharField(
        label="Płatność",
        max_length=64,
        required=True,
        widget=forms.HiddenInput(),
    )
    name = forms.CharField(
        label="Odbiorca",
        max_length=128,
        required=True,
        widget=forms.HiddenInput(),
    )
    name_long = forms.CharField(
        label="Odbiorca c.d.",
        max_length=128,
        required=False,
        widget=forms.HiddenInput(),
    )
    nip = forms.CharField(
        label="Nip", max_length=13, required=False, widget=forms.HiddenInput()
    )
    phone = forms.CharField(
        label="Telefon",
        max_length=18,
        required=True,
        widget=forms.HiddenInput(),
    )
    inpost_box = forms.CharField(
        label="Paczkomat",
        max_length=64,
        required=False,
        initial="",
        widget=forms.HiddenInput(),
    )
    street = forms.CharField(
        label="Ulica",
        max_length=128,
        required=False,
        widget=forms.HiddenInput(),
    )
    city = forms.CharField(
        label="Miasto",
        max_length=128,
        required=False,
        widget=forms.HiddenInput(),
    )
    products_total = forms.DecimalField(
        label="Produkty",
        decimal_places=2,
        required=False,
        widget=forms.HiddenInput(),
    )
    delivery_cost = forms.DecimalField(
        label="Dostawa",
        decimal_places=2,
        required=False,
        widget=forms.HiddenInput(),
    )
    payment_cost = forms.DecimalField(
        label="Płatność",
        decimal_places=2,
        required=False,
        widget=forms.HiddenInput(),
    )
    order_total_price = forms.FloatField(
        label="Suma zamówienia", required=False, widget=forms.HiddenInput()
    )


CHOICES = (
    ("Paragon", "1"),
    ("Faktura", "2"),
)

CHOICES_2 = [("M", "Male"), ("F", "Female")]


class OrderDetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop("client")
        super(OrderDetailsForm, self).__init__(*args, **kwargs)
        if self.client:
            if self.client.profile.company:
                CHOICES = (
                    ("Paragon", "1"),
                    ("Faktura", "2"),
                )
                self.fields["bill_select"] = forms.CharField(
                    label="Dokument handlowy",
                    widget=forms.Select(choices=CHOICES),
                    required=True,
                )
            else:
                CHOICES = (("Paragon", "1"),)
                self.fields["bill_select"] = forms.CharField(
                    label="Dokument handlowy",
                    widget=forms.Select(choices=CHOICES),
                    required=True,
                )
    phone_number = forms.CharField(label="Numer telefonu", required=True)
    delivery_method = forms.ModelChoiceField(
        label="Sposób dostawy",
        queryset=DeliveryMethod.objects.all(),
        required=True,
    )

    

    payment_method = forms.ModelChoiceField(
        label="Sposób płatności",
        queryset=PayMethod.objects.all(),
        required=True,
    )
