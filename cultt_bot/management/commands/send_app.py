import json
from django.core.management import BaseCommand

from cultt_bot.amo_crm import AmoCrmSession
from cultt_bot.models import CategoryOptions, BrandOptions, ModelsOption, SellApplication


class Command(BaseCommand):
    def handle(self, *args, **options):
        apps = [4587]

        for app_id in apps:
            application = SellApplication.objects.get(pk=app_id)
            amo_crm_session = AmoCrmSession('thecultt.amocrm.ru')
            result = amo_crm_session.create_leads_complex(application.id, application.user)

            if json.loads(result).get('title') == 'Unauthorized':
                if amo_crm_session.get_access_token('refresh_token'):
                    amo_crm_session.create_leads_complex(application.id, application.user)

            print(result)
