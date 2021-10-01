from PIL import Image
from django.views import View
from django.shortcuts import render, redirect
from web.models import Images
from web.models.products import Products

class First_Page(View):
    def get(self, request):
        img_carousel = Images.objects.filter(carousel=True)
        recommended_product = Products.objects.filter(is_promo=True).order_by('created_time')[:8]
        ctx = {'images_carousel': img_carousel,
                'recommended_product': recommended_product}
        return render(request, "front_page/first_page.html", ctx)


first_page = First_Page.as_view()