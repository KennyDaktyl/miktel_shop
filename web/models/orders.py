from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django_resized import ResizedImageField
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from web.constans import ORDER_STATUS, PAY_METHOD, PAY_ORDER_STATUS

from .base import BaseModel
from .products import file_size


class PayMethod(BaseModel):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(verbose_name="Numer wyświetlania")
    name = models.CharField(verbose_name="Nazwa metody płatności", max_length=64)
    pay_method = models.IntegerField(
        verbose_name="Rodzaj płatności", choices=PAY_METHOD
    )
    image = ResizedImageField(
        verbose_name="Zdjęcie główne",
        size=[1280, 960],
        upload_to="images/products/",
        validators=[file_size],
        null=True,
        blank=True,
    )
    link = models.URLField(verbose_name="Link do regulaminu", null=True, blank=True)
    price = models.DecimalField(
        verbose_name="Cena zamówienia",
        default=0.00,
        decimal_places=2,
        max_digits=7,
    )
    default = models.BooleanField(verbose_name="Czy domyślny?", default=False)
    is_active = models.BooleanField(verbose_name="Czy aktualna", default=True)

    def save(self, *args, **kwargs):
        if self.default is True:
            all_methods = PayMethod.objects.exclude(pk=self.id)
            for el in all_methods:
                el.default = False
                el.save()
        super(PayMethod, self).save(*args, **kwargs)

    def total_income(self, orders):
        orders_in_this_pay_m = orders.filter(pay_method=self)
        orders_realised = orders_in_this_pay_m.filter(status=4)
        pm_income_all_count = orders_in_this_pay_m.count()
        pm_income_closed_count = orders_realised.count()
        if orders_realised.aggregate(Sum("total_price"))["total_price__sum"]:
            _sum = orders_realised.aggregate(Sum("total_price"))["total_price__sum"]
        else:
            _sum = 0.00

        return [self.name, pm_income_all_count, pm_income_closed_count, _sum]

    class Meta:
        ordering = ("-number",)
        verbose_name_plural = "Rodzaje płatności"

    def __str__(self):
        return self.name


class DeliveryMethod(BaseModel):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(verbose_name="Numer wyświetlania")
    id_code = models.CharField(verbose_name="Kod dla id iframe inposta", max_length=64)
    name = models.CharField(verbose_name="Nazwa metody płatności", max_length=64)
    price = models.DecimalField(
        verbose_name="Cena za dostawę",
        default=0.00,
        decimal_places=2,
        max_digits=7,
    )
    price_promo = models.DecimalField(
        verbose_name="Cena promocyjna",
        default=0.00,
        decimal_places=2,
        max_digits=7,
    )
    price_netto = models.DecimalField(
        verbose_name="Cena netto",
        default=0.00,
        decimal_places=2,
        max_digits=7,
    )
    default = models.BooleanField(verbose_name="Czy domyślny?", default=False)
    inpost_box = models.BooleanField(
        verbose_name="Czy dostawa to paczkomat?", default=False
    )
    is_active = models.BooleanField(verbose_name="Czy aktualna?", default=True)

    def price_active(self, Cart):
        cart = Cart
        if cart.get_total_price() > 50.00:
            return self.price_promo
        else:
            return self.price

    def save(self, *args, **kwargs):
        if self.default is True:
            all_methods = DeliveryMethod.objects.exclude(pk=self.id)
            for el in all_methods:
                el.default = False
                el.save()
        self.price_netto = float(self.price) / 1.23
        super(DeliveryMethod, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-number",)
        verbose_name_plural = "Rodzaje dostawy"

    def __str__(self):
        return self.name

    @property
    def delivery_dict(self):
        return {
            "dm"
            + str(self.id): {
                "name": self.name.replace(" (*tylko przedpłata)", ""),
                "price": float(self.price),
                "price_netto": float(self.price_netto),
                "quantity": 1,
                "vat": 23,
                "total_vat": float(self.price) - float(self.price_netto),
                "t_netto": float(self.price_netto),
                "t_brutto": float(self.price),
            }
        }


# Pay_Method have to not NONE - order have to get pay_method id
class Orders(BaseModel):
    id = models.AutoField(primary_key=True)
    number = models.CharField(verbose_name="Numer zamówienia", max_length=64)

    pay_status = models.IntegerField(
        verbose_name="Status płatności", choices=PAY_ORDER_STATUS, default=1
    )
    status = models.IntegerField(
        verbose_name="Status zamówienia", choices=ORDER_STATUS, default=1
    )
    store = models.ForeignKey(
        "Store",
        on_delete=models.CASCADE,
        verbose_name="Magazyn",
        db_index=True,
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Klient",
        related_name="clinet_id",
    )
    delivery_method = models.ForeignKey(
        "DeliveryMethod",
        verbose_name="Rodzaj dostawy",
        on_delete=models.CASCADE,
    )
    pay_method = models.ForeignKey(
        "PayMethod", verbose_name="Rodzaj płatności", on_delete=models.CASCADE
    )
    payment_intent = models.CharField(
        "Id płatności w Stripe", null=True, blank=True, max_length=32
    )
    payment_success = models.BooleanField(
        verbose_name="Elektroniczna płatność udana", default=False
    )
    address = models.ForeignKey(
        "Address",
        on_delete=models.CASCADE,
        verbose_name="Adres dostawy",
        null=True,
        blank=True,
    )
    inpost_box = models.CharField(
        verbose_name="Numer paczkomatu", null=True, blank=True, max_length=64
    )
    phone_number = models.CharField(
        verbose_name="Numer telefonu", null=True, blank=True, max_length=12
    )
    start_delivery_time = models.TimeField(
        verbose_name="Czas wywozu", blank=True, null=True
    )
    sms_send = models.BooleanField(verbose_name="Sms", default=False)
    sms_time = models.TimeField(verbose_name="Czas smsa", blank=True, null=True)
    promo = models.BooleanField(verbose_name="Promocja", default=False)
    discount = models.IntegerField(verbose_name="Rabat", default=0)
    info = models.CharField(
        verbose_name="Informacje", max_length=256, null=True, blank=True
    )
    total_price = models.DecimalField(
        verbose_name="Cena zamówienia",
        default=0.00,
        decimal_places=2,
        max_digits=7,
    )
    products_item = models.JSONField(verbose_name="Produkty", null=True, blank=True)
    invoice_true = models.BooleanField(
        verbose_name="Czy wybrano fakturę", default=False
    )
    invoice = models.OneToOneField(
        "Invoices",
        verbose_name="Faktura",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def orders_closed(self):
        return self.objects.filter(status=5)

    def status_count(self, status):
        return self.objects.filter(status=status).count()

    def get_total_price_stripe(self):
        return int(self.total_price * 100)

    @property
    def get_total_price_netto(self):
        return round(float(self.total_price / Decimal(1.23)), 2)

    @property
    def get_invoice_total_price_netto(self):
        total_price = round(float(self.total_price / Decimal(1.23)), 2)
        delivery_method = DeliveryMethod.objects.get(name=self.delivery_method)
        return round(float(total_price) + float(delivery_method.price_netto), 2)

    @property
    def get_invoice_total_price(self):
        delivery_method = DeliveryMethod.objects.get(name=self.delivery_method)
        return round(float(self.total_price) + float(delivery_method.price_netto), 2)

    @property
    def get_invoice_total_vat(self):
        return round(
            float(self.get_invoice_total_price - self.get_invoice_total_price_netto),
            2,
        )

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = "Zamówienia"

    def __str__(self):
        return "{}-{}-{}".format(
            self.number, self.store.name, self.get_status_display()
        )


class ProductCopy(BaseModel):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(
        "Orders",
        verbose_name="Relacja do zamówienia",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product_id = models.ForeignKey(
        "Products",
        verbose_name="Relacja do produktu",
        on_delete=models.CASCADE,
    )

    qty = models.IntegerField(verbose_name="Ilość pozycji")
    price = models.DecimalField(
        verbose_name="Cena podstawowa",
        default=0,
        decimal_places=2,
        max_digits=7,
    )
    discount = models.IntegerField(verbose_name="Rabat", default=0)
    info = models.CharField(
        verbose_name="Informacje", max_length=256, null=True, blank=True
    )

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = "Pozycje rachunku"

    def __str__(self):
        if self.order_id:
            return "{}, {}".format(str(self.order), self.product.name)
        else:
            return "{}".format(self.product_id.name)


class Invoices(BaseModel):
    order = models.ForeignKey("Orders", on_delete=models.CASCADE, null=True, blank=True)
    number = models.CharField(max_length=64)
    override_number = models.CharField(verbose_name="Nadpisany numer faktury", max_length=64, null=True, blank=True)
    override_date = models.DateField(verbose_name="Nadpisana data faktury", null=True, blank=True)
    pdf = models.FileField(null=True, blank=True)

    class Meta:
        ordering = ("-created_time",)
        verbose_name_plural = "Faktury"

    def __str__(self):
        return str(self.pdf)


@receiver(pre_delete, sender=Invoices)
def mymodel_delete(sender, instance, **kwargs):
    instance.pdf.delete(False)


class IndexAlfa(models.Model):
    created_time = models.DateTimeField(default=timezone.now, db_index=True)
    name = models.CharField(
        verbose_name="Nazwa miejscowości", max_length=256, null=True, blank=True
    )
    slug = models.SlugField(verbose_name="Slug",
                            blank=True, null=True, max_length=128)
    city_one = models.ForeignKey('Citys', related_name='city_one', on_delete=models.CASCADE, null=True, blank=True)    
    city_two = models.ForeignKey(
        'Citys', related_name='city_two', on_delete=models.CASCADE, null=True, blank=True)
    city_three = models.ForeignKey(
        'Citys', related_name='city_three', on_delete=models.CASCADE, null=True, blank=True)
    city_four = models.ForeignKey(
        'Citys', related_name='city_four', on_delete=models.CASCADE, null=True, blank=True)
    city_five = models.ForeignKey(
        'Citys', related_name='city_five', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Index alpfa"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace("ł", "l"))
        citys = Citys.objects.filter(index_alfa=self)[0:5]
        try:
            self.city_one = citys[0]
        except:
            pass
        try:
            self.city_two = citys[1]
        except:
            pass
        try:
            self.city_three = citys[2]
        except:
            pass
        try:
            self.city_four = citys[3]
        except:
            pass
        try:
            self.city_five = citys[4]
        except:
            pass
        super(IndexAlfa, self).save()

    def get_absolute_url(self):
        return reverse(
            "index_city_detail_stamp_delivery",
            kwargs={
                "slug": self.slug,
                "pk": self.id,
            },
        )

    def citys_of_index(self):
        return Citys.objects.filter(index_alfa=self)

    def __str__(self):
        return str(self.name)


class Citys(models.Model):
    index_alfa = models.CharField(
        verbose_name="Index alfa", max_length=256, null=True, blank=True
    )
    name = models.CharField(
        verbose_name="Nazwa miejscowości", max_length=256, null=True, blank=True
    )
    slug = models.SlugField(verbose_name="Slug",
                            blank=True, null=True, max_length=128)
    rybna_area = models.BooleanField(
        verbose_name="Okolica Rybnej", default=False
    )
    created_time = models.DateTimeField(default=timezone.now, db_index=True)

    def get_absolute_url(self):
        return reverse(
            "city_details_stamp_delivery",
            kwargs={
                "slug": self.slug,
                "pk": self.id,
            },
        )

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Miasta"

    def save(self, *args, **kwargs):
        self.index_alfa = self.name[0]
        self.slug = slugify(self.name.replace("ł", "l"))
        super(Citys, self).save()

    def __str__(self):
        return str(self.name)
