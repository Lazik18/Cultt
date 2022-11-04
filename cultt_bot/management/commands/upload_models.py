import json

import pandas as pd
from django.core.management import BaseCommand

from cultt_bot.models import SellApplication


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = pd.read_excel('static/new_model.xlsx', sheet_name='list 1')

        print(data)
