from django.contrib import admin

from cultt_bot.models import *

admin.site.register(TelegramBot)
admin.site.register(TelegramUser)
admin.site.register(CategoryOptions)
admin.site.register(StateOptions)
admin.site.register(DefectOptions)
admin.site.register(AmoCRMData)
admin.site.register(CooperationOption)
admin.site.register(FAQFirstLevel)
admin.site.register(FAQSecondLevel)
admin.site.register(CRMStatusID)


@admin.register(SellApplication)
class SellApplicationAdmin(admin.ModelAdmin):
    change_list_template = "admin/model_change_list.html"
    list_display = ('pk', 'name', 'email', 'tel', 'active', 'date_create', 'date_send')
    search_fields = ('name', 'email', 'tel', 'amocrm_id')


@admin.register(AmoCRMLog)
class AmoCRMLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date', 'result')


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'dialogs_started', 'applications_sent', 'clicks_manager', 'date')


@admin.register(ModelsOption)
class ModelsOptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'brand')


@admin.register(TelegramLog)
class TelegramLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'date_create')


@admin.register(BrandOptions)
class BrandOptionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'is_visible')
    list_display_links = ('pk', 'name', 'category')
    list_filter = ('category', )


@admin.register(PhotoApplications)
class PhotoApplicationsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'application', 'date')
    list_display_links = ('pk', 'application', 'date')
    search_fields = ('application__pk',)
