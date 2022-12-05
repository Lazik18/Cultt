from django.core.management import BaseCommand

from cultt_bot.amo_crm import AmoCrmSession


class Command(BaseCommand):
    def handle(self, *args, **options):
        amo_crm_session = AmoCrmSession('thecultt.amocrm.ru')
        result = amo_crm_session.get_access_token()
        print(result)
