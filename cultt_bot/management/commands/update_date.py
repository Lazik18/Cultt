import datetime
import json
import time
from datetime import timedelta
import requests
from django.core.management import BaseCommand

from cultt_bot.amo_crm import AmoCrmSession
from cultt_bot.models import SellApplication


class Command(BaseCommand):
    def handle(self, *args, **options):
        applications = SellApplication.objects.exclude(amocrm_id=None)
        amo_crm_session = AmoCrmSession('thecultt.amocrm.ru')

        get_headers = {'Authorization': f'Bearer {amo_crm_session.amo_crm_data.access_token}',
                       'Cookie': 'user_lang=ru'}

        i = 0
        for application in applications:
            print(f'{i}/{len(applications)}')
            time.sleep(0.5)

            response = requests.request('GET',
                                        f'https://thecultt.amocrm.ru/api/v4/leads/{application.amocrm_id}',
                                        headers=get_headers)

            if response.status_code == 200:
                application.date_send = datetime.datetime.fromtimestamp(response.json()["created_at"])
