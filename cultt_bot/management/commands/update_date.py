import json
import time

import requests
from django.core.management import BaseCommand

from cultt_bot.amo_crm import AmoCrmSession
from cultt_bot.models import CategoryOptions, BrandOptions, ModelsOption, SellApplication


class Command(BaseCommand):
    def handle(self, *args, **options):
        applications = SellApplication.objects.exclude(amocrm_id=None)
        amo_crm_session = AmoCrmSession('thecultt.amocrm.ru')

        get_headers = {'Authorization': f'Bearer {amo_crm_session.amo_crm_data.access_token}',
                       'Cookie': 'user_lang=ru'}

        for application in applications:
            time.sleep(1)

            response = requests.request('GET',
                                        f'https://thecultt.amocrm.ru/api/v4/leads/{application.amocrm_id}',
                                        headers=get_headers)

            if response.status_code == 200:
                # application.date_send = response.json()
                print(response.json()["created_at"])
