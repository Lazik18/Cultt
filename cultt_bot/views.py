import mimetypes
import traceback

import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import unquote

from cultt_bot.messages import handler_call_back, handler_photo, handler_message
from cultt_bot.models import *
from cultt_bot.bot.cultt_bot import bot_logic
from cultt_bot.general_functions import *

import json
import requests
import os

import pwd, grp

from cultt_bot.amo_crm import AmoCrmSession
from django_project.settings import BASE_DIR


def debug_dec(func):
    def wrapper(*args, **kwargs):
        bot_settings = TelegramBot.objects.filter().first()
        bot = telepot.Bot(token=bot_settings.token)
        try:
            func(*args, **kwargs)
        except Exception as ex:
            TelegramLog.objects.create(text=repr(ex) + '\n' + traceback.format_exc())
    return wrapper


# Редирект в админку
def admin_redirect(request):
    return redirect('/admin/')


# Функция для ловли сообщений
@csrf_exempt
def web_hook_bot(request, bot_url):
    try:
        telegram_bot = TelegramBot.objects.get(url=bot_url)

        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))

            # Если пользователь нажал кнопку
            if 'callback_query' in data:
                # chat_id = data['callback_query']['from']['id']
                # chat_data = data['callback_query']['data']
                # message_id = data['callback_query']['message']['message_id']
                #
                # if str(chat_id) in ['673616491', '350436882', '5604116591']:
                #     handler_call_back(data)
                # else:
                #     bot_logic(telegram_bot.id, chat_id, chat_data, 'data', message_id)
                handler_call_back(data)
            # Если пользователь написал что-то
            if 'message' in data:
                if 'text' in data['message'].keys():
                    # chat_id = data['message']['chat']['id']
                    # chat_msg = data['message']['text']
                    # message_id = data['message']['message_id']
                    #
                    # if str(chat_id) in ['673616491', '350436882', '5604116591']:
                    #     handler_message(data)
                    # else:
                    #     bot_logic(telegram_bot.id, chat_id, chat_msg, 'message', message_id)
                    handler_message(data)

                elif 'photo' in data['message'].keys():
                    # chat_id = data['message']['chat']['id']
                    # photo_id = data['message']['photo'][len(data['message']['photo']) - 1]['file_id']
                    # message_id = data['message']['message_id']
                    #
                    # if str(chat_id) in ['673616491', '350436882', '5604116591']:
                    #     handler_photo(data)
                    # else:
                    #     bot_logic(telegram_bot.id, chat_id, photo_id, 'photo', message_id)
                    handler_photo(data)
                elif 'document' in data['message'].keys():
                    chat_id = data['message']['chat']['id']

                    telegram_bot.send_telegram_message(chat_id, 'Бот не поддерживает отправку файлов')

            return HttpResponse('ok', content_type="text/plain", status=200)
        else:
            if bot_url == 'test':
                # Сохраняем URL
                telegram_bot.url = random_string(length=20)
                telegram_bot.save()

                # Удалить старый web hook для бота
                requests.get(f'https://api.telegram.org/bot{telegram_bot.token}/deleteWebhook')
                # Добавить web_hook для бота
                url_bot = f'https://culttbotdev.ru/telegram_bot/{telegram_bot.url}'
                requests.get(f'https://api.telegram.org/bot{telegram_bot.token}/setWebhook?url={url_bot}')

            # Получаем информацию по веб хук
            req_text = requests.get(f'https://api.telegram.org/bot{telegram_bot.token}/getWebhookInfo').text

            return HttpResponse(req_text)
    except Exception as ex:
        TelegramLog.objects.create(text=traceback.format_exc())
        # bug_trap(additional_parameter=repr(ex) + '\n' + traceback.format_exc())

        return HttpResponse('ok', content_type="text/plain", status=200)


# Показать карточку заявки
def views_application(request, application_id):
    args = {
        'application': SellApplication.objects.get(id=application_id),
        'image_list': PhotoApplications.objects.filter(application__id=application_id)
    }

    return render(request, 'application_view.html', args)


# Для теста
def test(request):
    amo_crm_session = AmoCrmSession('thecultt.amocrm.ru')

    result = amo_crm_session.create_leads_complex(10)
    return HttpResponse(result, content_type="text/plain", status=200)


@csrf_exempt
@debug_dec
def web_hook_amocrm(request):
    telegram_bot = TelegramBot.objects.filter().first()

    if request.method == 'POST':
        data = unquote(request.body.decode('utf-8'))
        AmoCRMLog.objects.create(result=str(data))

        data = data.split('&')

        try:
            id_leads = data[0].split('=')[1]
        except:
            resp = {"status": "error",
                    "message": "no required fields"}
            return HttpResponse(str(resp), content_type="text/plain", status=200)

        try:
            status_id = data[1].split('=')[1]
        except:
            resp = {"status": "error",
                    "message": "no leads"}
            return HttpResponse(str(resp), content_type="text/plain", status=200)

        application = SellApplication.objects.get(amocrm_id=id_leads)
        status = CRMStatusID.objects.get(status_id=status_id)
        application.status = status.status_text
        application.save()

        if application.notifications:
            text_msg = f'{status.status_text}\n' \
                       f'Заявка №{application.amocrm_id}\n' \
                       f'Вариант сотрудничества: {application.cooperation_option.name}\n' \
                       f'Категория: {application.category.name}'
            telegram_bot.send_telegram_message(chat_id=application.user.chat_id, text=text_msg)

        resp = {"status": "success",
                "message": "ok"}
        return HttpResponse(str(resp), content_type="text/plain", status=200)


def download_file(request):
    filename = 'data.csv'
    filepath = BASE_DIR + '/static/' + filename

    df = pd.DataFrame(list(SellApplication.objects.all().values()))

    df.to_csv(filepath, index=False)

    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = f"attachment; filename={filename}"
    return response
