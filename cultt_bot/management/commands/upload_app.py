import pandas as pd
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = pd.read_excel('static/app.xlsx', sheet_name='Лист1')

        print(data)

        data1 = data[1].to_dict()

        for value in list(data1.values()):
            print(value)
