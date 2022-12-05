from django.core.management import BaseCommand

from cultt_bot.models import SellApplication


class Command(BaseCommand):
    def handle(self, *args, **options):
        applications = SellApplication.objects.all()

        for application in applications:
            application.status = 'Ваша заявка находится в обработке. Менеджер свяжется с вами в ближайшее время для обсуждения деталей.'
            application.save()
