import csv
from django.core.management.base import BaseCommand

from web.models.orders import (
    Citys
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        meta = {
            'file': "media/data/miasta_export.csv",
            'class': Citys,
            'fields': ('name', 'rybna_area')
        }

        f = open(meta['file'], 'w+')
        writer = csv.writer(f)
        writer.writerow(meta['fields'])
        for obj in meta['class'].objects.all():
            row = [(getattr(obj, field)) for field in meta['fields']]
            print(row)
            writer.writerow(row)
        f.close()
