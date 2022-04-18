from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand

from web.models.products import (
    Category,
    Products,
    Store,
    Colors,
    Brand,
    SubCategory,
    SubCategoryType,
    Vat,
    Size
)



class Command(BaseCommand):
    def handle(self, *args, **options):

        category = Category.objects.get(name="Dorabianie kluczy")
        sub_category = SubCategory.objects.get(name="Klucze mieszkaniowe")
        product_type = SubCategoryType()
        print(category, sub_category)

        file_path = "media/data/mag_klucze.csv"
        data = pd.read_csv(file_path, index_col=0)
        df = data.replace({np.nan: None})
        store = Store.objects.get(name="Serwis w Rybnej")
        tax = Vat.objects.get(name=23)
        date = datetime.now() - timedelta(days=1)
        # prod_to_del = Products.objects.filter(created_time__gte=date).delete()
        for index, row in df.iterrows():
            # row_category = mapping_category(row["Asortyment"])
            if row["Asortyment"] is not None:
                size, created = Size.objects.get_or_create(name=row["Size"])
                sub_cat_type, created = SubCategoryType.objects.get_or_create(
                    name=row["Asortyment"], sub_category=sub_category)
                # color, created = Colors.objects.get_or_create(name=row["Kolor"])
                brand = Brand.objects.get(name="Expres")
                created, product = Products.objects.get_or_create(
                    name=row["Nazwa"],
                    sub_category_type=sub_cat_type,
                    # code=row["Kod"],
                    size=size,
                    # price_netto_purchase=row["Cena net."],
                    qty=row["Ilość"],
                    price=row["Cena sprz"],
                    # color=color,
                    brand=brand,
                    image="images/products/no_image.webp",
                    tax=tax,
                    store=store,
                    discount=0,
                    is_active=True,
                )
                print(
                    row["Nazwa"],
                    row["Cena sprz"],
                    created
                    # row["Kod"],
                    # row["Ilość"],
                )
