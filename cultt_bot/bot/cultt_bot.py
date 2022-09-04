import traceback

from cultt_bot.models import *
from cultt_bot.general_functions import *

from pathlib import Path
from django.core.files import File

from cultt_bot.amo_crm import AmoCrmSession

import telepot
import json
import datetime

from datetime import timedelta

from telepot.namedtuple import ReplyKeyboardRemove


# Бот для взаимодействия с total coin
def bot_logic(bot_id, chat_id, chat_result, type_message, message_id):
    # Получаем данные бота
    telegram_bot = TelegramBot.objects.get(id=bot_id)
    # Авторизируемся в telegram api
    bot = telepot.Bot(telegram_bot.token)

    try:
        # Если пользователь пишет в первый раз создаем профиль
        if TelegramUser.objects.filter(chat_id=chat_id, bot=telegram_bot).count() == 0:
            TelegramUser.objects.create(
                bot=telegram_bot,
                chat_id=chat_id
            )

        if TelegramUser.objects.filter(chat_id=chat_id, bot=telegram_bot).count() == 1:
            user = TelegramUser.objects.get(chat_id=chat_id, bot=telegram_bot)

            if chat_result == '/start':
                user.step = 'start_message'
                user.save()

                SellApplication.objects.filter(user=user, active=True).delete()
            elif chat_result == 'Отменить заявку':
                user.step = 'cancel_application'
                user.save()

                SellApplication.objects.filter(user=user, active=True).delete()

            # Приветственное сообщение
            if user.step == 'start_message':
                start_message(bot_id, chat_id, chat_result, type_message, message_id)
            elif user.step == 'create_application':
                create_application(bot_id, chat_id, chat_result, type_message, message_id)
            elif user.step == 'cancel_application':
                start_message(bot_id, chat_id, chat_result, type_message, message_id)
            else:
                user.send_telegram_message('Ошибка шага')
        else:
            bot.sendMessage(chat_id=chat_id, text='Ошибка пользователя')

    except Exception:
        bug_trap()


# Приветственное сообщение
def start_message(bot_id, chat_id, chat_result, type_message, message_id):
    try:
        # Получаем данные бота
        telegram_bot = TelegramBot.objects.get(id=bot_id)
        # Пользователь
        user = TelegramUser.objects.get(chat_id=chat_id, bot=telegram_bot)

        if type_message == 'message':
            keyboard = build_keyboard('inline', [{f'{telegram_bot.start_button}': 'create_application_start_button'}],
                                      one_time=True)
            bot_text = telegram_bot.start_message

            if user.step == 'cancel_application':
                bot_text = telegram_bot.close_message

            user.send_telegram_message(bot_text, keyboard)
        else:
            if chat_result == 'create_application_start_button':
                user.step = 'create_application'
                user.save()

                create_application(bot_id, chat_id, chat_result, type_message, message_id)
            else:
                user.send_telegram_message('error start_message №1')
    except Exception:
        bug_trap()


def create_application(bot_id, chat_id, chat_result, type_message, message_id):
    try:
        # Получаем данные бота
        telegram_bot = TelegramBot.objects.get(id=bot_id)
        # Пользователь
        user = TelegramUser.objects.get(chat_id=chat_id, bot=telegram_bot)
        # Бот
        bot = telepot.Bot(telegram_bot.token)

        # Стандартное сообщение
        # Вариант сотрудничества
        def cooperation_option_message():
            message = telegram_bot.close_button
            keyboard = build_keyboard('reply', [{'Отменить заявку': 'Отменить заявку'},
                                                {'Связаться с менеджером': 'Связаться с менеджером'}],
                                      one_time=True)
            user.send_telegram_message(message, keyboard)

            bot_text = telegram_bot.cooperation_option_message

            button_list = []
            line_button = {}

            for cooperation_id in CooperationOption.objects.filter(is_visible=True):
                if len(line_button) < 1:
                    line_button[cooperation_id.name] = f'edit_application cooperation_option {cooperation_id.id}'
                else:
                    line_button[cooperation_id.name] = f'edit_application cooperation_option {cooperation_id.id}'
                    button_list.append(line_button)
                    line_button = {}

            if len(line_button) != 0:
                button_list.append(line_button)

            keyboard = build_keyboard('inline', button_list)

            user.send_telegram_message(bot_text, keyboard)

        # Введите имя
        def name_message():
            bot_text = telegram_bot.name_message
            user.send_telegram_message(bot_text)

        # Введите почту
        def email_message():
            bot_text = telegram_bot.email_message
            user.send_telegram_message(bot_text)

        # Введите номер телефона
        def tel_message():
            bot_text = telegram_bot.tel_message
            user.send_telegram_message(bot_text)

        # Выбор категории аксессуара
        def category_message():
            bot_text = telegram_bot.category_message

            button_list = []
            line_button = {}

            for category in CategoryOptions.objects.filter(is_visible=True):
                if len(line_button) < 1:
                    line_button[category.name] = f'edit_application category {category.id}'
                else:
                    line_button[category.name] = f'edit_application category {category.id}'
                    button_list.append(line_button)
                    line_button = {}

            if len(line_button) != 0:
                button_list.append(line_button)

            keyboard = build_keyboard('inline', button_list)

            user.send_telegram_message(bot_text, keyboard)

        # Выбор бренда
        def brand_message(letter=None):
            button_list = []
            line_button = {}
            bot_text = telegram_bot.brand_message

            # Достаем каждую букву
            if letter is None:
                letter_list = []

                for brand in BrandOptions.objects.filter(is_visible=True):
                    if brand.name[0].upper() not in letter_list:
                        letter_list.append(brand.name[0].upper())

                # Собираем клавиатуру
                for letter in letter_list:
                    if len(line_button) < 2:
                        line_button[letter] = f'edit_application brand {letter}'
                    else:
                        line_button[letter] = f'edit_application brand {letter}'
                        button_list.append(line_button)
                        line_button = {}

                if len(line_button) != 0:
                    button_list.append(line_button)
            else:
                for brand in BrandOptions.objects.filter(name__iregex=fr'^{letter}\w+'):
                    if len(line_button) < 1:
                        line_button[brand.name] = f'edit_application brand {brand.name[0]} {brand.id}'
                    else:
                        line_button[brand.name] = f'edit_application brand {brand.name[0]} {brand.id}'
                        button_list.append(line_button)
                        line_button = {}

                if len(line_button) != 0:
                    button_list.append(line_button)

                button_list.append({'Назад': 'edit_application'})

                button_list.append({'Нужный бренд не указан': 'edit_application site link'})

            keyboard = build_keyboard('inline', button_list)
            user.send_telegram_message(bot_text, keyboard)

        # Ввод модели
        def model_message():
            bot_text = telegram_bot.model_message
            user.send_telegram_message(bot_text)

        # Выбор состояние
        def state_message():
            bot_text = telegram_bot.state_message

            button_list = []
            line_button = {}

            for state in StateOptions.objects.filter(is_visible=True):
                if len(line_button) < 0:
                    line_button[state.name] = f'edit_application state {state.id}'
                else:
                    line_button[state.name] = f'edit_application state {state.id}'
                    button_list.append(line_button)
                    line_button = {}

            if len(line_button) != 0:
                button_list.append(line_button)

            keyboard = build_keyboard('inline', button_list)

            user.send_telegram_message(bot_text, keyboard)

        # Выбор наличие дефектов
        def defect_message():
            bot_text = telegram_bot.defect_message

            button_list = []
            line_button = {}

            for defect in DefectOptions.objects.filter(is_visible=True):
                if len(line_button) < 1:
                    line_button[defect.name] = f'edit_application defect {defect.id}'
                else:
                    line_button[defect.name] = f'edit_application defect {defect.id}'
                    button_list.append(line_button)
                    line_button = {}

            if len(line_button) != 0:
                button_list.append(line_button)

            keyboard = build_keyboard('inline', button_list)

            user.send_telegram_message(bot_text, keyboard)

        # Введите ожидания по цене
        def waiting_price_message():
            keyboard = build_keyboard('inline', [{f'{telegram_bot.help_to_evaluate}': 'help_to_evaluate_price'}],
                                      one_time=True)
            bot_text = telegram_bot.waiting_price_message
            user.send_telegram_message(bot_text, keyboard)

        # Загрузка фото
        def photo_message(photo=False):
            if not photo:
                bot_text = telegram_bot.photo_message_1

                user.send_telegram_message(bot_text)
            else:
                bot_text = telegram_bot.photo_message_2

                keyboard = build_keyboard('inline', [
                    {telegram_bot.end_photo_message: 'edit_application is_photo True'}
                ])

                user.send_telegram_message(bot_text, keyboard)

        # Подтверждение заявки
        def end_message():
            bot_text = 'Ваша заявка:\n\n'

            if application.cooperation_option.name is not None:
                bot_text += f'Вариант сотрудничества: {application.cooperation_option.name}\n'

            if application.name is not None:
                bot_text += f'Имя: {application.name}\n'

            if application.email is not None:
                bot_text += f'Почта: {application.email}\n'

            if application.tel is not None:
                bot_text += f'Телефон: {application.tel}\n'

            if application.category is not None:
                bot_text += f'Категория: {application.category.name}\n'

            if application.brand is not None:
                bot_text += f'Бренд: {application.brand.name}\n'

            if application.model is not None:
                bot_text += f'Модель: {application.model}\n'

            if application.state is not None:
                bot_text += f'Состояние: {application.state.name}\n'

            if application.defect is not None:
                bot_text += f'Наличие дефектов: {application.defect.name}\n'

            if application.waiting_price is not None:
                bot_text += f'Ожидание по цене: {application.waiting_price}\n'

            keyboard = build_keyboard('inline', [
                {'Отправить': 'edit_application end_message send'},
                # {'Отменить': 'edit_application end_message delete'}
            ])

            user.send_telegram_message(bot_text, keyboard)

            # application.delete()

            # user.step = 'start_message'
            # user.save()

        # Консьерж текст
        def concierge_message():
            bot_text = telegram_bot.concierge_message
            user.send_telegram_message(bot_text)

        # Если нет заявки то создаем ее
        application_count = SellApplication.objects.filter(user=user, active=True).count()

        if application_count == 0:
            SellApplication.objects.create(
                user=user
            )
        elif application_count > 1:
            SellApplication.objects.filter(user=user, active=True).delete()

            SellApplication.objects.create(
                user=user
            )

        # Получаем заявку пользователя
        application = SellApplication.objects.get(user=user, active=True)

        if chat_result == 'edit_application site link':
            bot_text = telegram_bot.not_brand
            keyboard = build_keyboard('inline', [
                {'Сайт': 'this_urlhttp://cultt.wemd.ru/'}
            ])
            user.send_telegram_message(bot_text, keyboard)

        # Для связи с менеджером
        elif chat_result == 'Связаться с менеджером':
            bot_text = telegram_bot.contact_manager
            user.send_telegram_message(bot_text)

        # Проверяем что еще не заполнено
        # Вариант сотрудничества
        elif application.cooperation_option is None:
            if type_message == 'message':
                cooperation_option_message()
            else:
                try:
                    bot.deleteMessage((chat_id, message_id))
                except telepot.exception.TelegramError:
                    pass

                if 'cooperation_option' in chat_result and CooperationOption.objects.filter(
                        id=chat_result.split(' ')[2]).count() == 1:
                    application.cooperation_option = CooperationOption.objects.get(id=chat_result.split(' ')[2])
                    application.save()

                    name_message()
                else:
                    cooperation_option_message()
        # Имя пользователя
        elif application.name is None:
            if type_message == 'message':
                if len(chat_result.split(' ')) == 2:
                    application.name = chat_result
                    application.save()

                    email_message()
                else:
                    bot_text = telegram_bot.error_name
                    user.send_telegram_message(bot_text)
            else:
                try:
                    bot.deleteMessage((chat_id, message_id))
                except telepot.exception.TelegramError:
                    pass

                name_message()
        # Почту пользователя
        elif application.email is None:
            if type_message == 'message':
                if email_validation(chat_result):
                    application.email = chat_result
                    application.save()

                    tel_message()
                else:
                    bot_text = telegram_bot.error_email
                    user.send_telegram_message(bot_text)
            else:
                try:
                    bot.deleteMessage((chat_id, message_id))
                except telepot.exception.TelegramError:
                    pass

                email_message()
        # Номер телефона пользователя
        elif application.tel is None:
            if type_message == 'message':
                if phone_number_validator(chat_result):
                    application.tel = chat_result
                    application.save()

                    if 'консьерж' in application.cooperation_option.name.lower():
                        concierge_message()
                    else:
                        category_message()
                else:
                    bot_text = telegram_bot.error_phone
                    user.send_telegram_message(bot_text)
            else:
                try:
                    bot.deleteMessage((chat_id, message_id))
                except telepot.exception.TelegramError:
                    pass

                tel_message()
        # Если ветка консьерж
        elif 'консьерж' in application.cooperation_option.name.lower() and application.concierge_count == 0:
            if type_message == 'message':
                application.concierge_count = chat_result
                application.save()

                end_message()
            else:
                try:
                    bot.deleteMessage((chat_id, message_id))
                except telepot.exception.TelegramError:
                    pass

                concierge_message()
        else:
            # Категория аксессуара
            if application.category is None and application.concierge_count == 0:
                if type_message == 'message':
                    category_message()
                else:
                    try:
                        bot.deleteMessage((chat_id, message_id))
                    except telepot.exception.TelegramError:
                        pass

                    if 'category' in chat_result and CategoryOptions.objects.filter(
                            id=chat_result.split(' ')[2]).count() == 1:
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        application.category = CategoryOptions.objects.get(id=chat_result.split(' ')[2])
                        application.save()

                        if application.category.id in [10, 11]:
                            brand_message()
                        else:
                            waiting_price_message()
                    else:
                        category_message()
            elif application.concierge_count == 0 and application.category.id in [10, 11]:
                # Бренд
                if application.brand is None and application.concierge_count == 0:
                    if type_message == 'message':
                        brand_message()
                    else:
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        if 'brand' in chat_result:
                            if len(chat_result.split(' ')) == 4:
                                if BrandOptions.objects.filter(id=chat_result.split(' ')[3]).count() == 1:
                                    application.brand = BrandOptions.objects.get(id=chat_result.split(' ')[3])
                                    application.save()

                                    model_message()
                                else:
                                    brand_message()
                            else:
                                brand_message(chat_result.split(' ')[2])
                        else:
                            brand_message()
                # Модель
                elif application.model is None and application.concierge_count == 0:
                    if type_message == 'message':
                        application.model = chat_result
                        application.save()

                        state_message()
                    else:
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        model_message()
                # Состояние
                elif application.state is None and application.concierge_count == 0:
                    if type_message == 'message':
                        state_message()
                    else:
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        if 'state' in chat_result and StateOptions.objects.filter(
                                id=chat_result.split(' ')[2]).count() == 1:
                            application.state = StateOptions.objects.get(id=chat_result.split(' ')[2])
                            application.save()

                            defect_message()
                        else:
                            try:
                                bot.deleteMessage((chat_id, message_id))
                            except telepot.exception.TelegramError:
                                pass

                            state_message()
                # Наличие дефектов
                elif application.defect is None and application.concierge_count == 0:
                    if type_message == 'message':
                        state_message()
                    else:
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        if 'defect' in chat_result and DefectOptions.objects.filter(
                                id=chat_result.split(' ')[2]).count() == 1:
                            application.defect = DefectOptions.objects.get(id=chat_result.split(' ')[2])
                            application.save()

                            waiting_price_message()
                        else:
                            defect_message()
                # Ожидание по цене
                elif application.waiting_price is None and application.concierge_count == 0:
                    if type_message == 'message':
                        if chat_result.isdecimal():
                            if int(chat_result) >= 1000:
                                application.waiting_price = chat_result
                                application.save()

                                photo_message()
                            else:
                                waiting_price_message()
                        else:
                            waiting_price_message()
                    elif type_message == 'data':
                        if chat_result == 'help_to_evaluate_price':
                            application.waiting_price = 0
                            application.save()

                            try:
                                bot.deleteMessage((chat_id, message_id))
                            except telepot.exception.TelegramError:
                                pass

                            photo_message()
                        else:
                            waiting_price_message()
                    else:
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        waiting_price_message()
                # Отправка фотографий
                elif not application.is_photo and application.concierge_count == 0:
                    if type_message == 'photo':
                        # Скачиваем фото
                        path = Path(f'application_image/{chat_result}.jpg')

                        bot.download_file(chat_result, path)

                        with path.open(mode='rb') as f:
                            PhotoApplications.objects.create(
                                application=application,
                                photo=File(f, name=path.name),
                            )

                            date_end = datetime.datetime.now()
                            date_start = date_end - timedelta(seconds=2)

                            if PhotoApplications.objects.filter(application=application, date__gte=date_start,
                                                                date__lte=date_end).count() < 2:
                                photo_message(photo=True)
                    elif type_message == 'data':
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        if 'is_photo' in chat_result:
                            application.is_photo = True
                            application.save()

                            end_message()
                        else:
                            photo_message()
                    else:
                        bot_text = telegram_bot.error_photo
                        user.send_telegram_message(bot_text)
                # Подтверждение заявки
                else:
                    if type_message == 'message':
                        end_message()
                    else:
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        if 'end_message' in chat_result:
                            if 'send' in chat_result:
                                application.active = False
                                application.save()

                                amo_crm_session = AmoCrmSession('thecultt.amocrm.ru')
                                result = amo_crm_session.create_leads_complex(application.id)

                                if json.loads(result).get('title') == 'Unauthorized':
                                    if amo_crm_session.get_access_token('refresh_token'):
                                        amo_crm_session.create_leads_complex(application.id)
                            else:
                                bot_text = telegram_bot.close_message
                                user.send_telegram_message(bot_text, ReplyKeyboardRemove())

                                application.delete()

                            user.step = 'start_message'
                            user.save()

                            keyboard = build_keyboard('reply', [{f'{telegram_bot.start_button}': 'create_application'}],
                                                      one_time=True)

                            user.send_telegram_message(telegram_bot.end_message, keyboard)
                        else:
                            cooperation_option_message()
            else:
                # Ожидание по цене
                if application.waiting_price is None:
                    if type_message == 'message':
                        if chat_result.isdecimal():
                            if int(chat_result) >= 1000:
                                application.waiting_price = chat_result
                                application.save()

                                photo_message()
                            else:
                                waiting_price_message()
                        else:
                            waiting_price_message()
                    elif type_message == 'data':
                        if chat_result == 'help_to_evaluate_price':
                            application.waiting_price = 0
                            application.save()

                            try:
                                bot.deleteMessage((chat_id, message_id))
                            except telepot.exception.TelegramError:
                                pass

                            photo_message()
                        else:
                            waiting_price_message()
                    else:
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        waiting_price_message()
                # Отправка фотографий
                elif not application.is_photo:
                    if type_message == 'photo':
                        # Скачиваем фото
                        path = Path(f'application_image/{chat_result}.jpg')

                        bot.download_file(chat_result, path)

                        with path.open(mode='rb') as f:
                            PhotoApplications.objects.create(
                                application=application,
                                photo=File(f, name=path.name),
                            )

                            date_end = datetime.datetime.now()
                            date_start = date_end - timedelta(seconds=2)

                            if PhotoApplications.objects.filter(application=application, date__gte=date_start,
                                                                date__lte=date_end).count() < 2:
                                photo_message(photo=True)
                    elif type_message == 'data':
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        if 'is_photo' in chat_result:
                            application.is_photo = True
                            application.save()

                            end_message()
                        else:
                            photo_message()
                    else:
                        bot_text = telegram_bot.error_photo
                        user.send_telegram_message(bot_text)
                # Подтверждение заявки
                else:
                    if type_message == 'message':
                        end_message()
                    else:
                        try:
                            bot.deleteMessage((chat_id, message_id))
                        except telepot.exception.TelegramError:
                            pass

                        if 'end_message' in chat_result:
                            if 'send' in chat_result:
                                application.active = False
                                application.save()

                                amo_crm_session = AmoCrmSession('thecultt.amocrm.ru')
                                result = amo_crm_session.create_leads_complex(application.id)

                                if json.loads(result).get('title') == 'Unauthorized':
                                    if amo_crm_session.get_access_token('refresh_token'):
                                        amo_crm_session.create_leads_complex(application.id)
                            else:
                                bot_text = telegram_bot.close_message
                                user.send_telegram_message(bot_text, ReplyKeyboardRemove())

                                application.delete()

                            user.step = 'start_message'
                            user.save()

                            keyboard = build_keyboard('reply', [{f'{telegram_bot.start_button}': 'create_application'}],
                                                      one_time=True)

                            user.send_telegram_message(telegram_bot.end_message, keyboard)
                        else:
                            cooperation_option_message()
    except Exception as ex:
        bug_trap(additional_parameter=traceback.format_exc())
