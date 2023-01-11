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
                if ModelsOption.objects.filter(brand=brand_option, name__istartswith=model[:-1]).exists():
                    print(f'Модель {model}')
                    model_option = ModelsOption.objects.filter(brand=brand_option, name__istartswith=model[:-1]).first()
                    model_option.have_offer_price = True

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Приоритет выкуп'].tolist()[0] is not None:
                        model_option.offer_priority = True

                    model_option.price_site_min = data[data['Бренд'] == brand][data['Модель'] == model]['Цена сайта min (базовая)'].tolist()[0]
                    model_option.price_site_max = data[data['Бренд'] == brand][data['Модель'] == model]['Цена сайта max (базовая)'].tolist()[0]

                    model_option.price_purchase_min = data[data['Бренд'] == brand][data['Модель'] == model]['Выплата по выкупу min'].tolist()[0]
                    model_option.price_purchase_max = data[data['Бренд'] == brand][data['Модель'] == model]['Выплата по выкупу max'].tolist()[0]

                    model_option.price_sale_min = data[data['Бренд'] == brand][data['Модель'] == model]['Выплата по реализации min'].tolist()[0]
                    model_option.price_sale_max = data[data['Бренд'] == brand][data['Модель'] == model]['Выплата по реализации max'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Размер S'].tolist()[0] != '-':
                        model_option.size_S = data[data['Бренд'] == brand][data['Модель'] == model]['Размер S'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Размер M'].tolist()[0] != '-':
                        model_option.size_M = data[data['Бренд'] == brand][data['Модель'] == model]['Размер M'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Размер L'].tolist()[0] != '-':
                        model_option.size_L = data[data['Бренд'] == brand][data['Модель'] == model]['Размер L'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Яркие/Лимитированные'].tolist()[0] != '-':
                        model_option.color_L = data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Яркие/Лимитированные'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Нейтральные'].tolist()[0] != '-':
                        model_option.color_N = data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Нейтральные'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Классические'].tolist()[0] != '-':
                        model_option.color_C = data[data['Бренд'] == brand][data['Модель'] == model]['Цвет Классические'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Винтаж'].tolist()[0] != '-':
                        model_option.state_V = data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Винтаж'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Хорошее'].tolist()[0] != '-':
                        model_option.state_G = data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Хорошее'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Отличное'].tolist()[0] != '-':
                        model_option.state_E = data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Отличное'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Новое с биркой'].tolist()[0] != '-':
                        model_option.state_N = data[data['Бренд'] == brand][data['Модель'] == model]['Состояние Новое с биркой'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Материал Текстиль/Рафия/PVX'].tolist()[0] != '-':
                        model_option.material_T = data[data['Бренд'] == brand][data['Модель'] == model]['Материал Текстиль/Рафия/PVX'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Материал Кожа/Замша'].tolist()[0] != '-':
                        model_option.material_L = data[data['Бренд'] == brand][data['Модель'] == model]['Материал Кожа/Замша'].tolist()[0]

                    if data[data['Бренд'] == brand][data['Модель'] == model]['Материал Экзотическая кожа'].tolist()[0] != '-':
                        model_option.material_EL = data[data['Бренд'] == brand][data['Модель'] == model]['Материал Экзотическая кожа'].tolist()[0]

                    model_option.save()

                else:
                    print(f'Модель {model} не найдена')
