from django import forms
from web.models import Products


class MainPhotoProductForm(forms.Form):
    image = forms.FileField(required=True, label="Ustaw foto główne")
    alt = forms.CharField(
        label="Alternatywny tekst dla foto głównego",
        required=True,
        max_length=64,
    )
    title = forms.CharField(
        label="Tytuł-tekst-dla-foto-głównego",
        required=True,
        max_length=64,
    )


class AddMainPhotoForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ('image', 'alt', 'title')
        labels = {
            "image": ("Dodaj zdjęcie główne"),
            "title": ("Dodaj title zdjęcia"),
            "alt": ("Dodaj tekst alternatywny"),
        }


class SelectDetailsProductForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ('brand', 'size', 'color', 'qty', 'price',
                  'discount', 'desc', 'is_recommended', 'is_news', 'is_promo')
        # labels = {
        #     "image": ("Dodaj zdjęcie główne"),
        #     "title": ("Dodaj title zdjęcia"),
        #     "alt": ("Dodaj tekst alternatywny"),
        # }
