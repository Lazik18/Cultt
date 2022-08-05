from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from cultt_bot.models import *
from cultt_bot.bot.cultt_bot import bot_logic
from cultt_bot.general_functions import *

import json
import requests
import os

import pwd, grp

from cultt_bot.amo_crm import AmoCrmSession


# Редирект в админку
def admin_redirect(request):
    SellApplication.objects.all().delete()
    return redirect('/admin/')


# Функция для ловли сообщений
@csrf_exempt
def web_hook_bot(request, bot_url):
    telegram_bot = TelegramBot.objects.get(url=bot_url)

    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))

            # Если пользователь нажал кнопку
            if 'callback_query' in data:
                chat_id = data['callback_query']['from']['id']
                chat_data = data['callback_query']['data']
                message_id = data['callback_query']['message']['message_id']

                bot_logic(telegram_bot.id, chat_id, chat_data, 'data', message_id)

            # Если пользователь написал что-то
            if 'message' in data:
                if 'text' in data['message'].keys():
                    chat_id = data['message']['chat']['id']
                    chat_msg = data['message']['text']
                    message_id = data['message']['message_id']

                    bot_logic(telegram_bot.id, chat_id, chat_msg, 'message', message_id)
                elif 'photo' in data['message'].keys():
                    chat_id = data['message']['chat']['id']
                    photo_id = data['message']['photo'][len(data['message']['photo']) - 1]['file_id']
                    message_id = data['message']['message_id']

                    bot_logic(telegram_bot.id, chat_id, photo_id, 'photo', message_id)

            return HttpResponse('ok', content_type="text/plain", status=200)
        else:
            if bot_url == 'test':
                # Сохраняем URL
                telegram_bot.url = random_string(length=20)
                telegram_bot.save()

                # Удалить старый web hook для бота
                requests.get(f'https://api.telegram.org/bot{telegram_bot.token}/deleteWebhook')
                # Добавить web_hook для бота
                url_bot = f'https://culttbot.ru/telegram_bot/{telegram_bot.url}'
                requests.get(f'https://api.telegram.org/bot{telegram_bot.token}/setWebhook?url={url_bot}')

            # Получаем информацию по веб хук
            req_text = requests.get(f'https://api.telegram.org/bot{telegram_bot.token}/getWebhookInfo').text

            return HttpResponse(req_text)
    except Exception:
        bug_trap()

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

