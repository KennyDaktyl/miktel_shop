from django import forms
from web.models import Products
from web.models.products import Images


class MainPhotoProductForm(forms.Form):
    image = forms.FileField(required=True, label="Ustaw foto główne")
    alt = forms.CharField(
        label="Alternatywny tekst dla foto głównego",
        required=False,
        max_length=64,
    )
    title = forms.CharField(
        label="Tytuł-tekst-dla-foto-głównego",
        required=False,
        max_length=64,
    )


class AddMainPhotoForm(forms.ModelForm):

    alt = forms.CharField(required=False)

    class Meta:
        model = Products
        fields = ("image", "alt", "title")
        labels = {
            "image": ("Dodaj zdjęcie"),
            "title": ("Dodaj title zdjęcia"),
            "alt": ("Dodaj tekst alternatywny"),
        }
        required = {"alt": False}

    def __init__(self, *args, **kwargs):
        super(AddMainPhotoForm, self).__init__(*args, **kwargs)
        self.fields["title"].required = False
        self.fields["alt"].required = False


class AddGalleryPhotoForm(forms.ModelForm):

    alt = forms.CharField(required=False)

    class Meta:
        model = Images
        fields = ("product", "image", "alt", "title")
        labels = {
            "image": ("Dodaj zdjęcie"),
            "title": ("Dodaj title zdjęcia"),
            "alt": ("Dodaj tekst alternatywny"),
        }
        required = {"alt": False}

    def __init__(self, *args, **kwargs):
        super(AddGalleryPhotoForm, self).__init__(*args, **kwargs)
        self.fields["title"].required = False
        self.fields["alt"].required = False


class SelectDetailsProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SelectDetailsProductForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Products
        fields = (
            "name",
            "sub_category_type",
            "brand",
            "size",
            "color",
            "qty",
            "price",
            "discount",
            "desc",
            "is_recommended",
            "is_news",
            "is_promo",
            "meta_description",
            "meta_title"
        )
