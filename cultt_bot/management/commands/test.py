import requests
from django.core.management import BaseCommand

from cultt_bot.amo_crm import AmoCrmSession


class Command(BaseCommand):
    def handle(self, *args, **options):
        amo_crm_data = AmoCrmSession('thecultt.amocrm.ru')
        headers = {
            'authorization': f'Bearer {amo_crm_data.get_access_token()}',
            'Content-Type': 'application/json'
        }

        resp = requests.get(f'https://thecultt.amocrm.ru/api/v4/contacts?filter[custom_fields_values][67727]=buzzina@rambler.ru', headers)
        print(resp.json())
