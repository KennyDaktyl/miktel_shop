from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand

from web.models.orders import (
    Citys
)


class Command(BaseCommand):
    def handle(self, *args, **options):

        file_path = "media/data/miasta_export.csv"
        data = pd.read_csv(file_path, index_col=0)
        df = data.replace({np.nan: None})
        for index, row in df.iterrows():
            # row_category = mapping_category(row["Asortyment"])
            city, created = Citys.objects.get_or_create(name=row["name"], rybna_area=row["rybna_area"])
            print(row["name"])
            print(created)