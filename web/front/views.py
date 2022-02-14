import random
from email.mime import image

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.views import View
from PIL import Image

from web.models import Images, articles
from web.models.articles import Articles
from web.models.products import Products

from .forms import *
from .functions import *


class FirstPage(View):
    def get(self, request):
        img_carousel = Images.objects.filter(carousel=True)

        qs = Products.objects.filter(is_recommended=True).exclude(
            image="images/products/no_image.webp"
        )
        possible_ids = list(qs.values_list("id", flat=True))
        possible_ids = random.sample(possible_ids, 8)
        random_recommended_products = qs.filter(pk__in=possible_ids)

        promo_products = Products.objects.filter(is_promo=True).order_by(
            "created_time"
        )[:8]
        articles = Articles.objects.all()
        ctx = {
            "images_carousel": img_carousel,
            "recommended_products": random_recommended_products,
            "promo_products": promo_products,
            "articles": articles,
        }
        return render(request, "front_page/first_page.html", ctx)


class ContactPage(View):
    def get(self, request):
        form = ContactForm()
        ctx = {"form": form}
        return render(request, "front_page/contact_page.html", ctx)

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            captcha = form.cleaned_data["captcha"]
            message += "\n" + "Email kontaktowy - " + str(email)
            msg = send_contact_message(
                subject,
                message,
            )
            print(msg)
            messages.success(request, "Wysyłanie email zakończnono poprawnie.")

            return redirect("contact_page")
        else:
            messages.error(request, "Wypełnij wszystkie pola formularza.")
            ctx = {"form": form}
            return render(request, "front_page/contact_page.html", ctx)


class PrivacyPolicyPage(View):
    def get(self, request):
        ctx = {}
        return render(request, "front_page/privacy_policy.html", ctx)


class TermsAndRulesPage(View):
    def get(self, request):
        ctx = {}
        return render(request, "front_page/terms_rules.html", ctx)


def error_404(request, exception):
    context = {}
    return render(request, "front_page/404.html", context)


def error_500(request):
    context = {}
    return render(request, "front_page/500.html", context)


first_page = FirstPage.as_view()
contact_page = ContactPage.as_view()
privacy_policy = PrivacyPolicyPage.as_view()
terms_rules = TermsAndRulesPage.as_view()
