
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand

from web.models.products import (
    Products
)


class Command(BaseCommand):
    def handle(self, *args, **options):

        file_path = "media/data/products.csv"
        data = pd.read_csv(file_path, index_col=0)
        df = data.replace({np.nan: None})
        for index, row in df.iterrows():
            product = Products.objects.get(id=row["id"])
            product.qty = 0
            product.save()