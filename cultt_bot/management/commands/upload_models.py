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
            print(f'Категория {category}')
            brands = list(set(data[data['Тип аксессуара'] == category]['Бренд'].tolist()))

            category_option = CategoryOptions.objects.filter(name=category).first()

            if category_option is None:
                print(f'Нет категории - {category}')
                continue

            for brand in brands:
                print(f'-{brand}')
                models = data[data['Тип аксессуара'] == category][data['Бренд'] == brand]['Модель'].tolist()

                brand_option = BrandOptions.objects.filter(category=category_option, name__in=brand).first()

                if brand_option is None:
                    brand_option = BrandOptions.objects.create(category=category_option, name=brand)
                    print(f'Создан бренд - {brand}')

                for model in models:
                    if model is not str:
                        continue

                    if ModelsOption.objects.exists(brand=brand_option, name__in=model):
                        print(f'Модель уже существует - {model}')
                        continue

                    ModelsOption.objects.create(brand=brand_option, name=model)
                    print(f'Модель создана - {model}')
