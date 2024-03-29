import mimetypes
import pandas as pd
from django.contrib import admin

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import re_path

from cultt_bot.models import *
from django_project.settings import BASE_DIR

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
admin.site.register(AccessoryMaterial)
admin.site.register(AccessoryColor)
admin.site.register(AccessorySize)


@admin.register(SellApplication)
class SellApplicationAdmin(admin.ModelAdmin):
    change_list_template = "admin/model_change_list.html"
    list_display = ('pk', 'name', 'email', 'tel', 'active', 'date_create', 'date_send')
    search_fields = ('name', 'email', 'tel', 'amocrm_id')
    list_filter = ('date_send',)

    def get_urls(self):
        urls = super(SellApplicationAdmin, self).get_urls()
        custom_urls = [re_path('^import/$', self.download, name='download'), ]
        return custom_urls + urls

    def download(self, request):
        return HttpResponseRedirect("/download")


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
