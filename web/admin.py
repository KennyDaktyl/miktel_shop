import os
from uuid import uuid4
from django.conf import settings
from django.contrib import admin
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from weasyprint import HTML

from web.models import *
from web.models.orders import IndexAlfaStamp

@admin.action(description='Utwórz profil')
def make_active(modeladmin, request, queryset):
    for user in queryset:
        token = ActivateToken.objects.create(
                    user=user,
                    activation_token=str(int(str(uuid4()).split("-")[0], 16)),
                )
        user.is_active = True
        user.email = user.username
        user.save()

class CustomUserAdmin(UserAdmin):
    list_display = [f.name for f in User._meta.fields]
    search_fields = ("username",)
    list_display_links = ('username',)
    exclude = ['pk']
    actions = [make_active]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Articles._meta.fields]
    list_display_links = ('title',)
    list_filter = ("category",)
    search_fields = ("title",)
    exclude = ['pk']

@admin.register(ActivateToken)
class ActivateTokenAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ActivateToken._meta.fields]
    search_fields = ("user",)
    list_display_links = ('activation_token',)
    exclude = ['pk']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Profile._meta.fields]
    list_filter = ("company",)
    list_display_links = ('user',)
    search_fields = (
        "last_name",
        "username",
        "nip_number",
    )
    exclude = ['pk']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Address._meta.fields]
    list_filter = (
        # 'workplace',
        # 'worker_position',
    )
    search_fields = ("user_id",)
    list_display_links = ('user',)
    exclude = ['pk']

@admin.register(PayMethod)
class PayMethonAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PayMethod._meta.fields]
    list_display_links = ('name',)
    exclude = ['pk']

@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DeliveryMethod._meta.fields]
    list_display_links = ('name',)
    exclude = ['pk']

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Orders._meta.fields]
    list_filter = (
        "store",
        "pay_method",
    )
    list_display_links = ('number',)
    search_fields = ("number",)
    exclude = ['pk']

@admin.register(ProductCopy)
class ProductCopyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProductCopy._meta.fields]
    exclude = ["order", "pk"]

# Register your models here.


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Store._meta.fields]
    exclude = ['pk']
    list_display_links = ('name',)

@admin.register(Colors)
class ColorsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Colors._meta.fields]
    exclude = ['pk']
    list_display_links = ('name',)

@admin.register(Vat)
class VatAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Vat._meta.fields]
    exclude = ['pk']
    list_display_links = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Brand._meta.fields]
    exclude = ['pk']
    list_display_links = ('name',)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Products._meta.fields]
    list_filter = (
        "store_id",
        "is_top",
        "is_recommended",
        "is_news",
        "is_promo",
        "sub_category_type"

    )
    search_fields = ("name", "pk", )
    list_display_links = ('name',)
    exclude = ['pk']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Size._meta.fields]
    # list_filter = ('sub_category', )
    search_fields = ("name",)
    list_display_links = ('name',)
    exclude = ['pk']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]
    search_fields = ("name",)
    list_display_links = ('name',)
    exclude = ['pk']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SubCategory._meta.fields]
    search_fields = ("name",)
    list_display_links = ('name',)
    exclude = ['pk']


@admin.register(SubCategoryType)
class SubCategoryTypeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SubCategoryType._meta.fields]
    list_display_links = ('name',)
    search_fields = ("name",)
    exclude = ['pk']

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Images._meta.fields]
    list_display_links = ('image',)
    exclude = ['pk']
    # list_filter = ('post', )
    # search_fields = ('post', )


@admin.action(description='Utwórz fakturę')
def create_invoice(modeladmin, request, queryset):
    for invoice in queryset:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT + str(invoice.pdf)))
        except OSError:
            pass
        if invoice.override_number:
            file_name = "pdf/faktura-" + invoice.override_number + ".pdf"
            invoice.pdf = file_name
            invoice.save()
        context = {"order": invoice.order, "invoice": invoice}
        html_string = render_to_string("orders/invoice.html", context)
        html = HTML(string=html_string)
        if invoice.override_number:
            html.write_pdf(target=settings.MEDIA_ROOT + file_name)
        else:
            html.write_pdf(target=settings.MEDIA_ROOT + str(invoice.pdf))

@admin.register(Invoices)
class InvoicesAdmin(admin.ModelAdmin):
    # list_display = [f.name for f in Invoices._meta.fields]
    list_display = ('number', 'created_time', 'pdf')
    list_display_links = ('number',)
    exclude = ['pk']
    # list_filter = ('post', )
    # search_fields = ('post', )
    actions = [create_invoice,]


@admin.register(IndexAlfaStamp)
class IndexAlfaStampAdmin(admin.ModelAdmin):
    # list_display = [f.name for f in Citys._meta.fields]
    list_display = ('name', 'city_one', 'city_two',
                    'city_three', 'city_four', 'city_five', )
    list_display_links = ('name',)
    exclude = ['pk']
    search_fields = ('name', )


@admin.register(Citys)
class CitysAdmin(admin.ModelAdmin):
    # list_display = [f.name for f in Citys._meta.fields]
    list_display = ('name', 'rybna_area')
    list_display_links = ('name',)
    exclude = ['pk']
    list_filter = ('rybna_area', )
    search_fields = ('name', )
