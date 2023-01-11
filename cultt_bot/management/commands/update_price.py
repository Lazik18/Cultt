import pandas as pd
from django.core.management import BaseCommand

from cultt_bot.models import CategoryOptions, BrandOptions, ModelsOption


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = pd.read_csv('static/price.csv')

        print(data)

        brands = list(set(data['Бренд'].tolist()))

        category_option = CategoryOptions.objects.filter(name='Женские сумки').first()

        if category_option is None:
            print('Нет категории')
            return

        for brand in brands:
            print(f'Бренд: {brand}')
            models = data[data['Бренд'] == brand]['Модель'].tolist()

            brand_option = BrandOptions.objects.filter(category=category_option, name__istartswith=brand).first()

            for model in models:
                if ModelsOption.objects.filter(brand=brand_option, name__istartswith=model).exists():
                    print(f'Модель {model}')
                    model_option = ModelsOption.objects.filter(brand=brand_option, name__istartswith=model).first()
                    model_option.have_offer_price = True

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Приоритет выкуп'] is not None:
                        model_option.offer_priority = True

                    model_option.price_site_min = data[data['Бренд'] == brand][data['Модель'] == model]['Цена сайта min (базовая)']
                    model_option.price_site_max = data[data['Бренд'] == brand][data['Модель'] == model]['Цена сайта max (базовая)']

                    model_option.price_purchase_min = data[data['Бренд'] == brand][data['Модель'] == model]['Выплата по выкупу min']
                    model_option.price_purchase_max = data[data['Бренд'] == brand][data['Модель'] == model]['Выплата по выкупу max']

                    model_option.price_sale_min = data[data['Бренд'] == brand][data['Модель'] == model]['Выплата по реализации min']
                    model_option.price_sale_max = data[data['Бренд'] == brand][data['Модель'] == model]['Выплата по реализации max']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Размер S'] != '-':
                        model_option.size_S = data[data['Бренд'] == brand][data['Модель'] == model]['Размер S']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Размер M'] != '-':
                        model_option.size_M = data[data['Бренд'] == brand][data['Модель'] == model]['Размер M']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Размер L'] != '-':
                        model_option.size_L = data[data['Бренд'] == brand][data['Модель'] == model]['Размер L']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Яркие/Лимитированные'] != '-':
                        model_option.color_L = data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Яркие/Лимитированные']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Нейтральные'] != '-':
                        model_option.color_N = data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Нейтральные']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Классические'] != '-':
                        model_option.color_C = data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Классические']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Винтаж'] != '-':
                        model_option.state_V = data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Винтаж']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Хорошее'] != '-':
                        model_option.state_G = data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Хорошее']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Отличное'] != '-':
                        model_option.state_E = data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Отличное']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Новое с биркой'] != '-':
                        model_option.state_N = data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Новое с биркой']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Материал Текстиль/Рафия/PVX'] != '-':
                        model_option.material_T = data[data['Бренд'] == brand][data['Модель'] == model]['Материал Текстиль/Рафия/PVX']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Материал Кожа/Замша'] != '-':
                        model_option.material_L = data[data['Бренд'] == brand][data['Модель'] == model]['Материал Кожа/Замша']

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Материал Экзотическая кожа'] != '-':
                        model_option.material_EL = data[data['Бренд'] == brand][data['Модель'] == model]['Материал Экзотическая кожа']
