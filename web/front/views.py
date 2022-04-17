import random
import os

# from csp.decorators import csp_update
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from web.models import Images
from web.models.articles import Articles
from web.models.orders import IndexAlfaStamp, Citys
from web.models.products import Products


from .forms import ContactForm
from .functions import send_contact_message, send_email_contact_message_by_django


class FirstPage(View):
    def get(self, request):
        img_carousel_first = Images.objects.filter(carousel=True).first()
        img_carousel = Images.objects.filter(carousel=True)[1:]

        qs = Products.objects.filter(is_recommended=True).exclude(
            image="images/products/no_image.webp"
        )
        possible_ids = list(qs.values_list("id", flat=True))
        possible_ids = random.sample(possible_ids, 8)
        random_recommended_products = qs.filter(pk__in=possible_ids)
        is_top = Products.objects.filter(is_top=True)
        promo_products = Products.objects.filter(is_promo=True).order_by(
            "created_time"
        )[:8]
        articles = Articles.objects.all()
        ctx = {
            "image_carousel_first": img_carousel_first,
            "images_carousel": img_carousel,
            "top_products": is_top,
            "recommended_products": random_recommended_products,
            "promo_products": promo_products,
            "articles": articles,
            "app_id": os.environ.get("APP_ID"),
        }
        return render(request, "front_page/first_page.html", ctx)


# @method_decorator(
#     csp_update(
#         FRAME_SRC=["'self' https://www.google.com/recaptcha/",
#                   "https://www.google.com/maps/"]
#     ),
#     name="dispatch",
# )
class ContactPage(View):
    def get(self, request):
        form = ContactForm()
        ctx = {"form": form, "public_key": settings.RECAPTCHA_PUBLIC_KEY}
        return render(request, "front_page/contact_page.html", ctx)

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            message += "\n" + "Email kontaktowy - " + str(email)
            send_contact_message(
                subject,
                message,
            )
            # send_email_contact_message_by_django(subject, message)
            messages.success(request, "Wysyłanie email zakończnono poprawnie.")

            return redirect("contact_page")
        else:
            messages.error(request, "Wypełnij wszystkie pola formularza.")
            ctx = {"form": form, "public_key": settings.RECAPTCHA_PUBLIC_KEY}
            return render(request, "front_page/contact_page.html", ctx)


class PrivacyPolicyPage(View):
    def get(self, request):
        ctx = {}
        return render(request, "front_page/privacy_policy.html", ctx)


class TermsAndRulesPage(View):
    def get(self, request):
        ctx = {}
        return render(request, "front_page/terms_rules.html", ctx)


class IndexCitysStamDelivery(ListView):
    template_name = "front_page/index_list_citys.html"
    # paginate_by = 20
    model = IndexAlfaStamp


class IndexCityDetailsStamDelivery(DetailView):
    template_name = "front_page/index_details_stamp_delivery.html"
    # paginate_by = 20
    model = IndexAlfaStamp


class CityDetailsStamDelivery(DetailView):
    template_name = "front_page/city_details_stamp_delivery.html"
    # paginate_by = 20
    model = Citys


def error_404(request, exception):
    context = {}
    return render(request, "front_page/404.html", context, status=404)


def error_500(request):
    context = {}
    return render(request, "front_page/500.html", context, status=500)


first_page = FirstPage.as_view()
contact_page = ContactPage.as_view()
privacy_policy = PrivacyPolicyPage.as_view()
terms_rules = TermsAndRulesPage.as_view()
index_citys_stamp_delivery = IndexCitysStamDelivery.as_view()
index_city_detail_stamp_delivery = IndexCityDetailsStamDelivery.as_view()
city_details_stamp_delivery = CityDetailsStamDelivery.as_view()
