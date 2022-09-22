from django.contrib import admin

from cultt_bot.models import *

admin.site.register(TelegramBot)
admin.site.register(TelegramUser)
admin.site.register(CategoryOptions)
admin.site.register(BrandOptions)
admin.site.register(StateOptions)
admin.site.register(DefectOptions)
admin.site.register(PhotoApplications)
admin.site.register(AmoCRMData)
admin.site.register(CooperationOption)


@admin.register(SellApplication)
class SellApplicationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'tel', 'active', 'date_create')
    search_fields = ('name', 'email', 'tel')


@admin.register(AmoCRMLog)
class AmoCRMLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date', 'result')


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'dialogs_started', 'applications_sent', 'clicks_manager', 'date')
