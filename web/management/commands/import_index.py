from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand

from web.models.orders import (
    IndexAlfaStamp
)


class Command(BaseCommand):
    def handle(self, *args, **options):

        file_path = "media/data/index_alfa.csv"
        data = pd.read_csv(file_path, index_col=0)
        df = data.replace({np.nan: None})
        for index, row in df.iterrows():
            # row_category = mapping_category(row["Asortyment"])
            index_alfa, created = IndexAlfaStamp.objects.get_or_create(
                name=row["Nazwa"])
            print(row["Nazwa"])
            print(created)
