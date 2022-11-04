import json

import pandas as pd
from django.core.management import BaseCommand

from cultt_bot.models import CategoryOptions, BrandOptions, ModelsOption


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = pd.read_excel('static/new_model.xlsx', sheet_name='list 1')

        print(data)

        print(data['Тип аксессуара'].to_dict())
