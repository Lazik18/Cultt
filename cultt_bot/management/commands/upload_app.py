import pandas as pd
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = pd.read_excel('static/app.xlsx', sheet_name='Лист1')

        print(data)

        data1 = data[1].to_dict()

        for value in data1.items():
            print(value)
