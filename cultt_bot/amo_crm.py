import traceback

from cultt_bot.models import *
from cultt_bot.conf import cultt_telegram_bot_token

import requests
import json
import telepot
import time
import datetime


# Для отравки уведомлений Илье и тестов
def send_telegram_error_message(message):
    bot = telepot.Bot(cultt_telegram_bot_token)
    bot.sendMessage(chat_id=673616491, text=f'Только для Ильи:\n{message}')


# Для работы с API
class AmoCrmSession:
    def __init__(self, sub_domain_name):
        self.amo_crm_data = AmoCRMData.objects.get(sub_domain=sub_domain_name)

        self.sub_domain = sub_domain_name
        self.client_id = self.amo_crm_data.client_id
        self.client_secret = self.amo_crm_data.client_secret
        self.code = self.amo_crm_data.code
        self.redirect_uri = self.amo_crm_data.redirect_uri
        self.refresh_token = self.amo_crm_data.refresh_token

    # Обмен кода авторизации на access token и refresh token
    def get_access_token(self, grant_type='authorization_code', double=False):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": grant_type,
            "redirect_uri": self.redirect_uri
        }

        if grant_type == 'authorization_code':
            data['code'] = self.code
        elif grant_type == 'refresh_token':
            data['refresh_token'] = self.refresh_token

        result = requests.post('https://thecultt.amocrm.ru/oauth2/access_token', data).text

        if 'access_token' in result:
            result = json.loads(result)

            self.amo_crm_data.access_token = result['access_token']
            self.amo_crm_data.refresh_token = result['refresh_token']
            self.amo_crm_data.save()

            return True
        else:
            # send_telegram_error_message(result)

            if not double:
                if grant_type == 'authorization_code':
                    return self.get_access_token('refresh_token', True)
                else:
                    return self.get_access_token('authorization_code', True)

    # Создать заявку
    def create_leads_complex(self, application_id, user):
        headers = {
            'authorization': f'Bearer {self.amo_crm_data.access_token}',
            'Content-Type': 'application/json'
        }

        application = SellApplication.objects.get(id=application_id)

        presentDate = datetime.datetime.now()
        unix_timestamp = datetime.datetime.timestamp(presentDate) * 1000

        if application.cooperation_option.name.lower() == 'консьерж':
            data = [{
                "source_uid": "telegram bot",
                "source_name": "Заявка из TelegramBot",
                "pipeline_id": application.cooperation_option.amocrm_pipeline_id,
                "_embedded": {
                    "leads": [{
                        "name": "Заявка из TelegramBot",
                        "created_by": 0,
                        "custom_fields_values": [
                            {
                                "field_id": 905517,
                                "values": [{"value": application.cooperation_option_name()}, ]
                            },
                            {
                                "field_id": 904727,
                                "values": [{"value": str(application.concierge_count)}, ]
                            },
                            {
                                "field_id": 904993,
                                "values": [{"value": str(user.username)}, ]
                            }

                        ],
                        "_embedded": {
                            "tags": [
                                {
                                    "name": application.cooperation_option.amocrm_tag
                                },
                                {
                                    "name": "Чат-бот"
                                }
                            ]
                        }
                    }],
                    "contacts": [{
                        "first_name": application.name,
                        "last_name": application.surname,
                        "custom_fields_values": [
                            {
                                "field_id": 67725,
                                "values": [{"value": application.tel}, ]
                            },
                            {
                                "field_id": 67727,
                                "values": [{"value": application.email}, ]
                            }
                        ]
                    }]
                },
                "metadata": {
                    "form_id": "telegram bot",
                    "form_name": "telegram bot",
                    "form_page": "telegram bot",
                    "form_sent_at": int(unix_timestamp),
                    "referer": "telegram bot"
                }
            }]
        else:
            data = [{
            "source_uid": "telegram bot",
            "source_name": "Заявка из TelegramBot",
            "pipeline_id": application.cooperation_option.amocrm_pipeline_id,
            "_embedded": {
                "leads": [{
                    "name": "Заявка из TelegramBot",
                    "created_by": 0,
                    "custom_fields_values": [
                        {
                            "field_id": 905517,
                            "values": [{"value": application.cooperation_option_name()}, ]
                        },
                        {
                            "field_id": 904321,
                            "values": [{"value": application.category.name}, ]
                        },
                        {
                            "field_id": 904323,
                            "values": [{"value": application.brand_name()}, ]
                        },
                        {
                            "field_id": 904325,
                            "values": [{"value": application.model}, ]
                        },
                        {
                            "field_id": 904327,
                            "values": [{"value": application.state_name()}, ]
                        },
                        {
                            "field_id": 904329,
                            "values": [{"value": application.defect_name()}, ]
                        },
                        {
                            "field_id": 904331,
                            "values": [{"value": str(application.waiting_price)}, ]
                        },
                        {
                            "field_id": 904333,
                            "values": [{"value": f"https://culttbot.ru/views/application/{application.id}"}, ]
                        }
                    ],
                    "_embedded": {
                        "tags": [
                            {
                                "name": application.cooperation_option.amocrm_tag
                            },
                            {
                                "name": "Чат-бот"
                            }
                        ]
                    }
                }],
                "contacts": [{
                    "first_name": application.name,
                    "last_name": application.surname,
                    "custom_fields_values": [
                        {
                            "field_id": 67725,
                            "values": [{"value": application.tel}, ]
                        },
                        {
                            "field_id": 67727,
                            "values": [{"value": application.email}, ]
                        }
                    ]
                }]
            },
            "metadata": {
                "form_id": "telegram bot",
                "form_name": "telegram bot",
                "form_page": "telegram bot",
                "form_sent_at": int(unix_timestamp),
                "referer": "telegram bot"
            }
        }]

        resp = requests.get(f'https://thecultt.amocrm.ru/api/v4/contacts?filter[custom_fields_values][67727]={application.email}', headers=headers)
        if resp.status_code == 204:
            data[0]['_embedded']['contacts'][0]['_embedded']['tags'][0] = "Новая регистрация"
        elif user.amocrm_id is None:
            try:
                user.amocrm_id = int(resp.json()['_embedded']['contacts'][0]['account_id'])
                user.save()
            except Exception as ex:
                TelegramLog.objects.create(text=repr(ex) + '\n' + traceback.format_exc())

        if user.amocrm_id is not None:
            data[0]['_embedded']['contacts'][0]['id'] = user.amocrm_id

        if user.username is not None:
            data[0]['_embedded']['leads'][0]['custom_fields_values'].append({
                            "field_id": 904993,
                            "values": [{"value": user.username}, ]
                        })

        result = requests.post(f'https://{self.sub_domain}/api/v4/leads/unsorted/forms', headers=headers, json=data)

        AmoCRMLog.objects.create(result=str(result.json()))

        if 'Can not found linked entities by id' in str(result.json()):
            user.amocrm_id = None
            user.save()
            return self.create_leads_complex(application_id, user)

        try:
            user.amocrm_id = int(result.json()['_embedded']['unsorted'][0]['_embedded']['contacts'][0]['id'])
            user.save()
        except:
            pass

        try:
            application.amocrm_id = int(result.json()['_embedded']['unsorted'][0]['_embedded']['leads'][0]['id'])
            application.save()
        except Exception as ex:
            TelegramLog.objects.create(text=repr(ex) + '\n' + traceback.format_exc())

        return result.text
