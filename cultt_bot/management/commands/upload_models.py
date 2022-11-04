import json

import pandas as pd
from django.core.management import BaseCommand

from cultt_bot.models import CategoryOptions, BrandOptions, ModelsOption


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = pd.read_excel('static/new_model.xlsx', sheet_name='list 1')

        print(data)

        categories = list(set(data['Тип аксессуара'].tolist()))

        for category in categories:
            print(f'{category}')
            brands = list(set(data[data['Тип аксессуара'] == category]['Бренд'].tolist()))

            for brand in brands:
                print(f'-{brand}')
                models = data[data['Тип аксессуара'] == category][data['Бренд'] == brand]['Модель'].tolist()

                for model in models:
                    print(f'--{model}')
