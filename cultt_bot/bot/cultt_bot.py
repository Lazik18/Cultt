from cultt_bot.models import *
from cultt_bot.general_functions import *

import telepot


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

            # Приветственное сообщение
            if user.step == 'start_message':
                start_message(bot_id, chat_id, chat_result, type_message, message_id)
            elif user.step == 'create_application':
                create_application(bot_id, chat_id, chat_result, type_message, message_id)
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
            if chat_result == telegram_bot.start_button:
                user.step = 'create_application'
                user.save()

                create_application(bot_id, chat_id, chat_result, type_message, message_id)
            else:
                keyboard = build_keyboard('reply', [{f'{telegram_bot.start_button}': 'create_application'}])

                user.send_telegram_message(telegram_bot.start_message, keyboard)
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
            bot_text = 'Выберите вариант сотрудничества'

            keyboard = build_keyboard('inline', [
                {'trade in': 'edit_application cooperation_option trade_in'},
                {'круговорот': 'edit_application cooperation_option circulation'}
            ])

            user.send_telegram_message(bot_text, keyboard)

        # Введите имя
        def name_message():
            bot_text = 'Введите имя'
            user.send_telegram_message(bot_text)

        # Введите почту
        def email_message():
            bot_text = 'Введите электронную почту'
            user.send_telegram_message(bot_text)

        # Введите номер телефона
        def tel_message():
            bot_text = 'Введите номер телефона'
            user.send_telegram_message(bot_text)

        # Выбор категории аксессуара
        def category_message():
            bot_text = 'Категория'

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
            bot_text = 'Выберите бренд'

            # Достаем каждую букву
            if letter is None:
                letter_list = []

                for brand in BrandOptions.objects.filter(is_visible=True):
                    if brand.name[0] not in letter_list:
                        letter_list.append(brand.name[0])

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

            keyboard = build_keyboard('inline', button_list)
            user.send_telegram_message(bot_text, keyboard)

        # Выбор модели
        def model_message():
            bot_text = 'Укажите модель вашего аксессуара'
            user.send_telegram_message(bot_text)

        # Выбор состояние
        def state_message():
            bot_text = 'Состояние'

            button_list = []
            line_button = {}

            for state in StateOptions.objects.filter(is_visible=True):
                if len(line_button) < 1:
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
            bot_text = 'Наличие дефектов'

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
            bot_text = 'Ваши ожидание по цене'
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

        # Проверяем что еще не заполнено
        # Вариант сотрудничества
        if application.cooperation_option is None:
            if type_message == 'message':
                cooperation_option_message()
            else:
                try:
                    bot.deleteMessage((chat_id, message_id))
                except telepot.exception.TelegramError:
                    pass

                if 'cooperation_option' in chat_result:
                    application.cooperation_option = chat_result.split(' ')[2]
                    application.save()

                    name_message()
                else:
                    cooperation_option_message()
        # Имя пользователя
        elif application.name is None:
            if type_message == 'message':
                application.name = chat_result
                application.save()

                email_message()
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
                    bot_text = "Некорректный email, напишите еще раз"
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

                    category_message()
                else:
                    bot_text = "Некорректный номер телефона, напишите еще раз"
                    user.send_telegram_message(bot_text)
            else:
                try:
                    bot.deleteMessage((chat_id, message_id))
                except telepot.exception.TelegramError:
                    pass

                tel_message()
        # Категория аксессуара
        elif application.category is None:
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

                    brand_message()
                else:
                    category_message()
        # Бренд
        elif application.brand is None:
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
        elif application.model is None:
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
        elif application.state is None:
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
        elif application.defect is None:
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
        elif application.waiting_price is None:
            if type_message == 'message':
                if chat_result.isdecimal():
                    application.waiting_price = chat_result
                    application.save()

                    application.delete()

                    state_message()
                else:
                    waiting_price_message()
            else:
                try:
                    bot.deleteMessage((chat_id, message_id))
                except telepot.exception.TelegramError:
                    pass

                waiting_price_message()
    except Exception:
        bug_trap()