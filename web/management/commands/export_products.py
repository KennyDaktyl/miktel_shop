import csv
from django.core.management.base import BaseCommand

from web.models.products import (
    Products
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        meta = {
            'file': "media/data/products.csv",
            'class': Products,
            'fields': ('id', 'sub_category_type', 'name', 'qty', "price")
        }

        f = open(meta['file'], 'w+')
        writer = csv.writer(f)
        writer.writerow(meta['fields'])
        for obj in meta['class'].objects.filter(qty__gt=0):
            row = [(getattr(obj, field)) for field in meta['fields']]
            print(row)
            writer.writerow(row)
        f.close()
