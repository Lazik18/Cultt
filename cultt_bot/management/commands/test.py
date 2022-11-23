import requests
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        resp = requests.get(f'https://thecultt.amocrm.ru/api/v4/contacts?filter[custom_fields_values][67727]=buzzina@rambler.ru')
        print(resp)
