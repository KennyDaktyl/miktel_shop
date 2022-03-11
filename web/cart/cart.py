from django.conf import settings
from web.models import Products
from web.products.serializers import ProductSerializer


class Cart(object):
    def __init__(self, request):
        """
        Inicjalizacja koszyka z produktami
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # zapis pustego koszyka w sesji
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Dodanie produktu do koszyka lub edycja parametrów
        """
        if str(product.id) in self.cart:
            if update_quantity:
                self.cart[str(product.id)]["quantity"] = int(quantity)
                qty = int(self.cart[str(product.id)]["quantity"])
            else:
                qty = int(self.cart[str(product.id)]["quantity"])
                self.cart[str(product.id)]["quantity"] = qty + int(quantity)
            qty = int(self.cart[str(product.id)]["quantity"])
            self.cart[str(product.id)]["price"] = float(product.price_promo)
            self.cart[str(product.id)]["price_netto"] = round(
                float(product.price_promo) / float("1." + "23"), 2
            )
            total_netto = round(
                ((float(self.cart[str(product.id)]["price_netto"])) * qty), 2
            )
            self.cart[str(product.id)]["t_netto"] = total_netto
            total_brutto = round(((float(product.price_promo)) * qty), 2)
            self.cart[str(product.id)]["t_brutto"] = total_brutto
            self.cart[str(product.id)]["discount"] = float(product.discount)
            self.cart[str(product.id)]["vat"] = product.tax.name
            self.cart[str(product.id)]["total_vat"] = round(
                (total_brutto - total_netto), 2
            )
            self.cart[str(product.id)]["name"] = product.name
            self.save()
        else:
            self.cart[str(product.id)] = {
                "quantity": str(quantity),
                "price": str(product.price_promo),
                "discount": str(product),
            }
            self.cart[str(product.id)]["price"] = float(product.price_promo)
            self.cart[str(product.id)]["price_netto"] = round(
                float(product.price_promo) / float("1." + "23"), 2
            )
            total_netto = round(
                ((float(self.cart[str(product.id)]["price_netto"])) * int(quantity)),
                2,
            )
            self.cart[str(product.id)]["t_netto"] = total_netto
            total_brutto = round(((float(product.price_promo)) * int(quantity)), 2)
            self.cart[str(product.id)]["t_brutto"] = total_brutto
            self.cart[str(product.id)]["discount"] = float(product.discount)
            self.cart[str(product.id)]["quantity"] = int(quantity)
            self.cart[str(product.id)]["vat"] = product.tax.name
            self.cart[str(product.id)]["total_vat"] = round(
                (total_brutto - total_netto), 2
            )
            self.cart[str(product.id)]["name"] = product.name
            self.save()

    def remove(self, product):
        """
        Usuwanie produktu z koszyka
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price_netto(self):
        """
        Obliczanie wartości koszyka wraz z rabatem
        """
        _sum = sum(
            (
                float(item["price_netto"])
                * (float((100 - float(item["discount"])) / 100))
                * int(item["quantity"])
            )
            for item in self.cart.values()
        )
        return round(float(_sum), 2)

    def get_total_price(self):
        """
        Obliczanie wartości koszyka wraz z rabatem
        """

        _sum = sum(
            (float(item["price"]) * int(item["quantity"]))
            for item in self.cart.values()
        )
        return round(float(_sum), 2)

    def __iter__(self):
        """
        Iterowanie po produktach w koszyku i pobieranie dancyh z bazy
        """
        products_ids = self.cart.keys()
        products = Products.objects.filter(pk__in=products_ids)
        cart = self.cart.copy()
        for product in products:
            product_serial = ProductSerializer(product)
            cart[str(product.id)]["product"] = product_serial.data

        for item in cart.values():
            item["image"] = item["product"]["image"].replace("/media/", "")
            item["price"] = float(item["price"])
            item["price_netto"] = round(float(item["price"] / float("1." + "23")), 2)
            item["discount"] = int(item["discount"])
            item["total_price_netto"] = round(
                float(int(item["quantity"]) * float((item["price_netto"]))), 2
            )
            item["total_price"] = item["price"] * item["quantity"]
            item["vat"] = item["product"]["tax"]
            yield item

    def get_products(self):
        return self.cart

    def len(self):
        """
        Obliczanie sumy elementów w koszyku
        """

        return sum(item["quantity"] for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def clear(self):
        """Usunięcie koszyka z sesji"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
