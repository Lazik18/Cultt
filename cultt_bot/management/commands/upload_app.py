import pandas as pd
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = pd.read_excel('static/app.xlsx', sheet_name='Лист1')

        print(data)

        data1 = list(data[1].to_dict())

        print(data1)

        for i in data1:
            print(i)
