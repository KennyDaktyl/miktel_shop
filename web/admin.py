from django.contrib import admin
from web.models.accounts import Profile, Address
from web.models.orders import PayMethod, DeliveryMethod, Orders, ProductCopy
from web.models import Products, Size, Category, Store, Vat, Images, Brand, Colors

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Profile._meta.fields]
    list_filter = (
        'company',
    )
    search_fields = (
        'last_name',
        'username',
        'nip_number',
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Address._meta.fields]
    list_filter = (
        # 'workplace',
        # 'worker_position',
    )
    search_fields = ('user_id', )



@admin.register(PayMethod)
class PayMethonAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PayMethod._meta.fields]


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DeliveryMethod._meta.fields]


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Orders._meta.fields]
    list_filter = (
        'store',
        'pay_method',
    )
    search_fields = ('number', )


@admin.register(ProductCopy)
class ProductCopyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProductCopy._meta.fields]
    exclude = ['order']

from django.contrib import admin

# Register your models here.



@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Store._meta.fields]


@admin.register(Colors)
class ColorsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Colors._meta.fields]


@admin.register(Vat)
class VatAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Vat._meta.fields]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Brand._meta.fields]


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Products._meta.fields]
    list_filter = (
        'store_id',
        'category',
        'size',
    )
    search_fields = ('name', )


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Size._meta.fields]
    # list_filter = ('sub_category', )
    search_fields = ('name', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]
    search_fields = ('name', )


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Images._meta.fields]
    # list_filter = ('post', )
    # search_fields = ('post', )