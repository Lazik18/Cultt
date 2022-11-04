import json

import pandas as pd
from django.core.management import BaseCommand

from cultt_bot.amo_crm import AmoCrmSession
from cultt_bot.models import SellApplication


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = pd.read_excel('static/app.xlsx', sheet_name='Лист1')

        print(data)

        data1 = data[1].to_dict()

        for value in list(data1.values()):
            app = SellApplication.objects.get(pk=value)

            amo_crm_session = AmoCrmSession('thecultt.amocrm.ru')
            result = amo_crm_session.create_leads_complex(value, app.user)

            if json.loads(result).get('title') == 'Unauthorized':
                if amo_crm_session.get_access_token('refresh_token'):
                    amo_crm_session.create_leads_complex(value, app.user)

            print(f'{value} OK\n')

        print('OK')
