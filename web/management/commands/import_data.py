import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand, CommandError

from web.models.products import Category, SubCategory, SubCategoryType


def mapping_category(cat_row):
    cat = {
        "5D": "Szkło hartowane 5D",
        "ADAPTERY": "Adaptery",
        "AUX": "AUX",
        "TRANSMITERY": "Transmitery",
        "ALKALICZNE": "Baterie alkaiczne",
        "IPHONE": "Baterie Iphone",
        "FAKE": "Baterie",
        "ORIGINAL": "Baterie",
        "ZAMIENNIKI": "Baterie",
        "FOLIA": "Folie ochronne",
        "Bezprzewodowe": "Głośniki bezprzewodowe",
        "INNE": "Inne",
        "HF": "Słuchawki HF",
        "HF BLUETOOTH": "Bluetooth",
        "INDUKCYJNE": "Ładowarki induk.",
        "JELLY": "Jelly Case",
        "ORYGINAŁ": "Case Oryginalne",
        "JELLY SPECJAL": "Jelly Case Special",
        "KABEL": "kable USB",
        "KABURA": "Kabury",
        "ORYGINAŁ KAB.": "Kabury Orygiał",
        "KABURA SEPCJAL": "Kabury special",
        "UNIWERSALNE": "Kabury uniwersalne",
        "ZAMIENNIKIII": "Ładowarka samochodowa",
        "ZAMIENNIK": "Ładowarka sieciowa",
        "USB 2.0": "Kara pamięci USB 2.0",
        "USB 3.0": "Kara pamięci USB 3.0",
        "POWERBANKI": "Powerbanki",
        "PREMIUMKI": "Ładowarka samochodowa",
        "SELFIESTICK": "Kijek selfie",
        "SPIGEN": "Futerały SPIGEN",
        "SZKŁO": "Szkło hartowane",
        "UV": "Folia UV",
        "GRAWITACYJNE": "Uchwyty samochodowe",
        "STANDARD": "Uchwyty samochodowe",
        "SPORT": "Uchwyty samochodowe",
        "MAGNETYCZNE": "Uchwyty samochodowe",
        "PREMIUMM": "Ładowarka samochodowa",
    }
    if cat_row in cat.keys():
        return cat[cat_row]


class Command(BaseCommand):
    def handle(self, *args, **options):

        category = Category.objects.get(name="Dorabianie kluczy")
        sub_category = SubCategory.objects.get(name="Klucze mieszkaniowe")
        product_type = SubCategoryType()
        print(category, sub_category)

        file_path = "media/data/mag_klucze.csv"
        data = pd.read_csv(file_path, index_col=0)
        df = data.replace({np.nan: None})
        for index, row in df.iterrows():
            row_category = mapping_category(row["Asortyment"])
            if row_category is not None:
                created, sub_cat = SubCategoryType.objects.get_or_create(
                    name=row_category, sub_category=sub_category
                )
                print(created, sub_cat)
