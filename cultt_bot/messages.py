import datetime
import json
from datetime import timedelta
import traceback
from pathlib import Path

import telepot
from django.core.files import File

from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

from cultt_bot.amo_crm import AmoCrmSession
from cultt_bot.models import TelegramBot, TelegramUser, SellApplication, CooperationOption, CategoryOptions, \
    BrandOptions, ModelsOption, StateOptions, DefectOptions, PhotoApplications, Indicator


def debug_dec(func):
    """
    Use for debug functions
    """
    def wrapper(*args, **kwargs):
        bot_settings = TelegramBot.objects.filter().first()
        bot = telepot.Bot(token=bot_settings.token)
        try:
            func(*args, **kwargs)
        except Exception as ex:
            bot.sendMessage(chat_id='673616491', text=repr(ex) + '\n' + traceback.format_exc())

    return wrapper


@debug_dec
def create_applications(user_telegram_id, coop_option_id, last_step=None, letter=None, finish_photo=False):
    bot_settings = TelegramBot.objects.filter().first()
    bot = telepot.Bot(token=bot_settings.token)

    user = TelegramUser.objects.get(chat_id=user_telegram_id)
    coop_option = CooperationOption.objects.filter(is_visible=True, pk=coop_option_id)

    if coop_option_id is None:
        bot.sendMessage(chat_id='Воспользуйтесь командой /start')
        return

    coop_option = coop_option.first()

    application, is_create = SellApplication.objects.get_or_create(user=user, active=True,
                                                                   cooperation_option=coop_option)

    if is_create:
        pass

    manager_keyboard = [InlineKeyboardButton(text=bot_settings.contact_to_manager, callback_data='ConnectManager')]
    cancel_keyboard = [InlineKeyboardButton(text=bot_settings.cancel_applications, callback_data='CancelApp')]

    if coop_option.count_accessory and application.concierge_count == 0:
        user.step = f'CountAccessory {coop_option_id}'
        user.save()

        keyboard = [manager_keyboard, cancel_keyboard]

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.concierge_message, reply_markup=keyboard)

        return
    elif coop_option.category and application.category is None:
        keyboard = []
        line_keyboard = []

        for category in CategoryOptions.objects.filter(is_visible=True):
            if len(line_keyboard) < 2:
                line_keyboard.append(InlineKeyboardButton(text=category.name,
                                                          callback_data=f'CreateApp Category {category.pk}'))
            else:
                line_keyboard.append(InlineKeyboardButton(text=category.name,
                                                          callback_data=f'CreateApp Category {category.pk}'))
                keyboard.append(line_keyboard)
                line_keyboard = []

        if len(line_keyboard) != 0:
            keyboard.append(line_keyboard)

        if last_step is not None:
            keyboard.append([InlineKeyboardButton(text=bot_settings.back_button, callback_data=f'BackApp {last_step}')])
        keyboard.append(manager_keyboard)
        keyboard.append(cancel_keyboard)

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.category_message, reply_markup=keyboard)
        return
    elif coop_option.brand and application.brand is None and application.category.have_brand:
        keyboard = []
        line_keyboard = []

        # Достаем каждую букву
        if letter is None:
            letter_list = []

            for brand in BrandOptions.objects.filter(is_visible=True):
                if brand.name[0].upper() not in letter_list:
                    letter_list.append(brand.name[0].upper())

            for letter in letter_list:
                if len(line_keyboard) < 3:
                    line_keyboard.append(InlineKeyboardButton(text=letter, callback_data=f'CreateApp Letter {letter}'))
                else:
                    line_keyboard.append(InlineKeyboardButton(text=letter, callback_data=f'CreateApp Letter {letter}'))
                    keyboard.append(line_keyboard)
                    line_keyboard = []

            if len(line_keyboard) != 0:
                keyboard.append(line_keyboard)
        else:
            for brand in BrandOptions.objects.filter(name__iregex=fr'^{letter}\w+'):
                if len(line_keyboard) < 2:
                    line_keyboard.append(InlineKeyboardButton(text=brand.name,
                                                              callback_data=f'CreateApp Brand {brand.id}'))
                else:
                    line_keyboard.append(InlineKeyboardButton(text=brand.name,
                                                              callback_data=f'CreateApp Brand {brand.id}'))
                    keyboard.append(line_keyboard)
                    line_keyboard = []

            if len(line_keyboard) != 0:
                keyboard.append(line_keyboard)

            keyboard.append([InlineKeyboardButton(text=bot_settings.brand_back_button,
                                                  callback_data=f'CreateApp')])

            keyboard.append([InlineKeyboardButton(text=bot_settings.brand_not_found,
                                                  callback_data=f'BrandNotFound')])

        if last_step is not None:
            keyboard.append([InlineKeyboardButton(text=bot_settings.back_button, callback_data=f'BackApp {last_step}')])
        keyboard.append(manager_keyboard)
        keyboard.append(cancel_keyboard)

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.brand_message, reply_markup=keyboard)
        return
    elif coop_option.model and application.model is None and application.category.have_brand:
        keyboard = []
        line_keyboard = []

        models_brand = ModelsOption.objects.filter(brand=application.brand)

        for model in models_brand:
            if len(line_keyboard) < 2:
                line_keyboard.append(InlineKeyboardButton(text=model.name, callback_data=f'CreateApp Model {model.pk}'))
            else:
                line_keyboard.append(InlineKeyboardButton(text=model.name, callback_data=f'CreateApp Model {model.pk}'))
                keyboard.append(line_keyboard)
                line_keyboard = []

        if len(line_keyboard) != 0:
            keyboard.append(line_keyboard)

        keyboard.append(InlineKeyboardButton(text='Я не знаю модель', callback_data=f'CreateApp Model NotKnow'))

        if last_step is not None:
            keyboard.append([InlineKeyboardButton(text=bot_settings.back_button, callback_data=f'BackApp {last_step}')])
        keyboard.append(manager_keyboard)
        keyboard.append(cancel_keyboard)

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.model_message, reply_markup=keyboard)
        return
    elif coop_option.state and application.state is None and application.category.have_brand:
        keyboard = []
        line_keyboard = []

        for state in StateOptions.objects.filter(is_visible=True):
            if len(line_keyboard) < 0:
                line_keyboard.append(InlineKeyboardButton(text=state.name, callback_data=f'CreateApp State {state.pk}'))
            else:
                line_keyboard.append(InlineKeyboardButton(text=state.name, callback_data=f'CreateApp State {state.pk}'))
                keyboard.append(line_keyboard)
                line_keyboard = []

        if len(line_keyboard) != 0:
            keyboard.append(line_keyboard)

        if last_step is not None:
            keyboard.append([InlineKeyboardButton(text=bot_settings.back_button, callback_data=f'BackApp {last_step}')])
        keyboard.append(manager_keyboard)
        keyboard.append(cancel_keyboard)

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.state_message, reply_markup=keyboard)
        return
    elif coop_option.defect and application.defect_finished is False and application.category.have_brand:
        keyboard = []
        line_keyboard = []

        for defect in DefectOptions.objects.filter(is_visible=True):
            if len(line_keyboard) < 1:
                text_data = defect.name
                if defect in application.defect.all():
                    text_data += ' ✅'
                line_keyboard.append(InlineKeyboardButton(text=text_data,
                                                          callback_data=f'CreateApp Defect {defect.pk}'))
            else:
                text_data = defect.name
                if defect in application.defect.all():
                    text_data += ' ✅'
                line_keyboard.append(InlineKeyboardButton(text=text_data,
                                                          callback_data=f'CreateApp Defect {defect.pk}'))
                keyboard.append(line_keyboard)
                line_keyboard = []

            if len(line_keyboard) != 0:
                keyboard.append(line_keyboard)

        text_defect_accept = 'Выбрать'
        if application.defect.count() < 1:
            text_defect_accept = 'Нет дефектов'

        keyboard.append(InlineKeyboardButton(text=text_defect_accept, callback_data='CreateApp Defect Accept'))

        if last_step is not None:
            keyboard.append([InlineKeyboardButton(text=bot_settings.back_button, callback_data=f'BackApp {last_step}')])
        keyboard.append(manager_keyboard)
        keyboard.append(cancel_keyboard)

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.defect_message, reply_markup=keyboard)
        return
    elif coop_option.price and application.waiting_price is None:
        keyboard = [[InlineKeyboardButton(text=bot_settings.help_to_evaluate, callback_data=f'CreateApp Price Help')]]

        user.step = f'WaitingPrice {coop_option_id}'
        user.save()

        if last_step is not None:
            keyboard.append([InlineKeyboardButton(text=bot_settings.back_button, callback_data=f'BackApp {last_step}')])
        keyboard.append(manager_keyboard)
        keyboard.append(cancel_keyboard)

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.waiting_price_message, reply_markup=keyboard)
        return
    elif coop_option.photo and application.is_photo is False:
        if not finish_photo:
            user.step = 'Photo'
            user.save()

            keyboard = []
            if last_step is not None:
                keyboard.append(
                    [InlineKeyboardButton(text=bot_settings.back_button, callback_data=f'BackApp {last_step}')])
            keyboard.append(manager_keyboard)
            keyboard.append(cancel_keyboard)

            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

            bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.photo_message_1, reply_markup=keyboard)
        else:
            keyboard = [[InlineKeyboardButton(text=bot_settings.end_photo_message, callback_data='CreateApp Photo')],
                        manager_keyboard, cancel_keyboard]

            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

            bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.photo_message_2, reply_markup=keyboard)
        return
    else:
        bot_text = bot_settings.applications_main_text + '\n\n'

        if application.cooperation_option.name is not None:
            bot_text += bot_settings.applications_cooperation_option + f': {application.cooperation_option.name}\n'

        if application.name is not None:
            bot_text += bot_settings.applications_name + f': {application.name}\n'

        if application.surname is not None:
            bot_text += bot_settings.applications_surname + f': {application.surname}\n'

        if application.email is not None:
            bot_text += bot_settings.applications_email + f': {application.email}\n'

        if application.tel is not None:
            bot_text += bot_settings.applications_tel + f': {application.tel}\n'

        if application.category is not None:
            bot_text += bot_settings.applications_category + f': {application.category.name}\n'

        if application.brand is not None:
            bot_text += bot_settings.applications_brand + f': {application.brand.name}\n'

        if application.brand is not None:
            bot_text += bot_settings.applications_model + f': {application.model}\n'

        if application.state is not None:
            bot_text += bot_settings.applications_state + f': {application.state.name}\n'

        if application.defect.count() >= 1:
            bot_text += bot_settings.applications_defect + ':'
            for defect_obj in application.defect.all():
                bot_text += f' {defect_obj.name.lower()},'
            bot_text = bot_text[:-1]
            bot_text += '\n'
        if application.waiting_price is not None:
            bot_text += bot_settings.applications_waiting_price + f': {application.waiting_price}₽\n'

        if application.concierge_count != 0:
            bot_text += bot_settings.applications_concierge_count + f': {application.concierge_count}\n'

        keyboard = [[InlineKeyboardButton(text=bot_settings.send_application_button, callback_data='SendApp')],
                    [InlineKeyboardButton(text=bot_settings.error_application, callback_data='EditApp')]]

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=bot_text, reply_markup=keyboard)



@debug_dec
def main_menu(user_telegram_id):
    bot_settings = TelegramBot.objects.filter().first()
    bot = telepot.Bot(token=bot_settings.token)

    user = TelegramUser.objects.get(chat_id=user_telegram_id)

    SellApplication.objects.filter(user=user, active=True).delete()

    coop_options = CooperationOption.objects.filter(is_visible=True)
    keyboard = []
    line_keyboard = []

    for option in coop_options:
        if len(line_keyboard) < 2:
            line_keyboard.append(InlineKeyboardButton(text=option.name, callback_data=f'CreateApp {option.pk}'))
        else:
            line_keyboard.append(InlineKeyboardButton(text=option.name, callback_data=f'CreateApp {option.pk}'))
            keyboard.append(line_keyboard)
            line_keyboard = []

    if len(line_keyboard) != 0:
        keyboard.append(line_keyboard)

    keyboard.append([InlineKeyboardButton(text=bot_settings.cancel_applications, callback_data='CancelApp')])
    keyboard.append([InlineKeyboardButton(text=bot_settings.contact_to_manager, callback_data='ConnectManager')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.cooperation_option_message, reply_markup=keyboard)


@debug_dec
def handler_command(data):
    bot_settings = TelegramBot.objects.filter().first()
    bot = telepot.Bot(token=bot_settings.token)

    command = data['message']['text']
    user_telegram_id = data['message']['chat']['id']

    user = TelegramUser.objects.get(chat_id=user_telegram_id)

    if command == '/start':
        text = bot_settings.start_message

        keyboard = [[InlineKeyboardButton(text=bot_settings.start_button, callback_data='MainMenu')]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=text, reply_markup=keyboard)
        SellApplication.objects.filter(user=user, active=True).delete()

        return


@debug_dec
def handler_message(data):
    bot_settings = TelegramBot.objects.filter().first()
    bot = telepot.Bot(token=bot_settings.token)

    message_text = data['message']['text']
    user_telegram_id = data['message']['chat']['id']

    try:
        user_telegram_username = data['message']['chat']['username']
    except KeyError:
        user_telegram_username = None

    user, is_create = TelegramUser.objects.get_or_create(chat_id=user_telegram_id)

    user.username = user_telegram_username
    user.save()

    if is_create is True:
        pass

    if message_text.startswith('/'):
        handler_command(data)
        return

    application = SellApplication.objects.filter(user=user, active=True)

    if application is None:
        bot.sendMessage(chat_id='Воспользуйтесь командой /start')
        return

    application = application.first()

    if 'CountAccessory' in user.step:
        try:
            if int(message_text) <= 0:
                raise ValueError('A small number')

            application.concierge_count = int(message_text)
            application.save()

            user.step = ''
            user.save()
        except:
            bot.sendMessage(chat_id=user_telegram_id, text='Некорректный ввод')

        create_applications(user_telegram_id, message_text.split()[1], last_step='Count')
        return
    elif 'WaitingPrice' in user.step:
        try:
            if int(message_text) < 1000:
                raise SyntaxError

            application.waiting_price = int(message_text)
            application.save()

            user.step = ''
            user.save()
        except ValueError:
            bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.waiting_price_message_incorrect_decimal)
        except SyntaxError:
            bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.waiting_price_message_incorrect_small)

        create_applications(user_telegram_id, message_text.split()[1], last_step='Price')
        return


@debug_dec
def handler_photo(data):
    bot_settings = TelegramBot.objects.filter().first()
    bot = telepot.Bot(token=bot_settings.token)

    user_telegram_id = data['callback_query']['message']['chat']['id']
    user = TelegramUser.objects.filter(chat_id=user_telegram_id)

    photo_id = data['message']['photo'][len(data['message']['photo']) - 1]['file_id']

    if user.step == 'Photo':
        application = SellApplication.objects.get(user=user, active=True)

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()

        path = Path(f'application_image/{photo_id}.jpg')

        bot.download_file(photo_id, path)

        with path.open(mode='rb') as f:
            PhotoApplications.objects.create(
                application=application,
                photo=File(f, name=path.name),
            )

            date_end = datetime.datetime.now()
            date_start = date_end - timedelta(seconds=2)

            if PhotoApplications.objects.filter(application=application, date__gte=date_start,
                                                date__lte=date_end).count() < 2:
                create_applications(user_telegram_id, application.cooperation_option.pk, finish_photo=True)




@debug_dec
def handler_call_back(data):
    bot_settings = TelegramBot.objects.filter().first()
    bot = telepot.Bot(token=bot_settings.token)

    user_telegram_id = data['callback_query']['message']['chat']['id']
    user_message_id = data['callback_query']['message']['message_id']

    user = TelegramUser.objects.filter(chat_id=user_telegram_id)

    if user is None:
        bot.sendMessage(chat_id='Воспользуйтесь командой /start')
        return
    else:
        user = user.first()

    try:
        user_telegram_username = data['callback_query']['message']['chat']['username']
        user.username = user_telegram_username
        user.save()
    except KeyError:
        pass
    except:
        return

    current_message = (user_telegram_id, user_message_id)
    button_press = data['callback_query']['data']

    application = SellApplication.objects.filter(user=user, active=True)

    if 'MainMenu' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass
        main_menu(user_telegram_id)
    elif 'ConnectManager' in button_press:
        pass
    elif 'CancelApp' in button_press:
        pass
    elif 'BackApp' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()

        if 'Category' in button_press:
            application.category = None
            application.save()

            create_applications(user_telegram_id, application.cooperation_option.pk)
            return
        elif 'Brand' in button_press:
            application.brand = None
            application.save()

            create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Category')
            return
        elif 'Model' in button_press:
            application.model = None
            application.save()

            create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Brand')
            return
        elif 'State' in button_press:
            application.state = None
            application.save()

            create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Model')
            return
        elif 'Defect' in button_press:
            application.defect_finished = False
            application.save()

            create_applications(user_telegram_id, application.cooperation_option.pk, last_step='State')
            return
        elif 'Price' in button_press:
            application.waiting_price = None
            application.save()

            if application.defect_finished:
                create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Defect')
            else:
                create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Category')

            return
        elif 'Count' in button_press:
            application.concierge_count = None
            application.save()

            create_applications(user_telegram_id, application.cooperation_option.pk)
            return

        return
    elif 'CrateApp Category' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()

        category_id = button_press.split()[2]

        application.category = CategoryOptions.objects.get(pk=category_id)
        application.save()

        create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Category')
        return
    elif 'CreateApp Letter' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()

        letter = button_press.split()[2]

        create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Category', letter=letter)
        return
    elif 'CreateApp Brand' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()

        brand_id = button_press.split()[2]
        application.brand = BrandOptions.objects.get(pk=brand_id)
        application.save()

        create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Brand')
        return
    elif 'BrandNotFound' in button_press:
        keyboard = [[InlineKeyboardButton(text='Ссылка', url='http://cultt.wemd.ru/')]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.not_brand, reply_markup=keyboard)
        return
    elif 'CreateApp Model' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()

        model_id = button_press.split()[2]
        if model_id == 'NotKnow':
            application.model = '-'
            application.save()
        else:
            application.model = ModelsOption.objects.get(pk=model_id).name
            application.save()

        create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Model')
        return
    elif 'CreateApp State' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()

        state_id = button_press.split()[2]
        application.state = StateOptions.objects.get(pk=state_id)
        application.save()

        create_applications(user_telegram_id, application.cooperation_option.pk, last_step='State')
        return
    elif 'CreateApp Defect' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()

        defect_id = button_press.split()[2]

        if defect_id == 'Accept':
            application.defect_finished = True
            application.save()

            create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Defect')
            return
        else:
            application.defect.add(DefectOptions.objects.get(pk=defect_id))
            application.save()

            create_applications(user_telegram_id, application.cooperation_option.pk, last_step='State')
            return
    elif 'CreateApp Price Help' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()
        application.waiting_price = 0
        application.save()

        user.step = ''
        user.save()

        create_applications(user_telegram_id, application.cooperation_option.pk, last_step='Price')
        return
    elif 'CreateApp Photo' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()

        application.is_photo = True
        application.save()

        user.step = ''
        user.save()

        create_applications(user_telegram_id, application.cooperation_option.pk)
        return
    elif 'SendApp' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        if application is None:
            bot.sendMessage(chat_id='Воспользуйтесь командой /start')
            return

        application = application.first()
        application.active = False
        application.save()

        amo_crm_session = AmoCrmSession('thecultt.amocrm.ru')
        result = amo_crm_session.create_leads_complex(application.id, user)

        stats = Indicator.objects.filter().last()
        stats.applications_sent += 1
        stats.save()

        if json.loads(result).get('title') == 'Unauthorized':
            if amo_crm_session.get_access_token('refresh_token'):
                amo_crm_session.create_leads_complex(application.id, user)

        keyboard = [[InlineKeyboardButton(text=bot_settings.start_button, callback_data='CreateApp')],
                    [InlineKeyboardButton(text=bot_settings.my_profile_button, callback_data='MyProfile')]]

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        bot.sendMessage(chat_id=user_telegram_id, text=bot_settings.end_message, reply_markup=keyboard)
    elif 'CreateApp' in button_press:
        try:
            bot.deleteMessage(current_message)
        except telepot.exception.TelegramError:
            pass

        option_id = button_press.split()[1]

        create_applications(user_telegram_id, option_id)
        return