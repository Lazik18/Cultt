from django.db import models

from telepot.exception import BotWasBlockedError

import telepot


class TelegramBot(models.Model):
    # Ссылка на бота
    link = models.TextField(blank=True, null=True, verbose_name='Ссылка на бота')
    # URL для бота
    url = models.TextField(verbose_name='URL для бота')
    # Токен бота
    token = models.TextField(verbose_name='Токен бота')

    # Текст бота
    # Приветственное сообщение
    start_message = models.TextField(verbose_name='Приветственное сообщение')
    # Стартовая кнопка (Продать вещи)
    start_button = models.TextField(verbose_name='Стартовая кнопка')
    # Отмена заявки
    close_button = models.TextField(verbose_name='Отмена заявки')
    # Текст после отмены
    close_message = models.TextField(verbose_name='Текст после отмены')
    # Вариант сотрудничества
    cooperation_option_message = models.TextField(default='Вариант сотрудничества', verbose_name='Вариант сотрудничества')
    # Введите имя
    name_message = models.TextField(default='Введите имя', verbose_name='Введите имя')
    # Введите почту
    email_message = models.TextField(default='Введите почту', verbose_name='Введите почту')
    # Введите номер телефона
    tel_message = models.TextField(default='Введите номер телефона', verbose_name='Введите номер телефона')
    # Выбор категории аксессуара
    category_message = models.TextField(default='Выбор категории аксессуара', verbose_name='Выбор категории аксессуара')
    # Выбор бренда
    brand_message = models.TextField(default='Выбор бренда', verbose_name='Выбор бренда')
    # Ввод модели
    model_message = models.TextField(default='Ввод модели', verbose_name='Ввод модели')
    # Выбор состояние
    state_message = models.TextField(default='Выбор состояние', verbose_name='Выбор состояние')
    # Выбор наличие дефектов
    defect_message = models.TextField(default='Выбор наличие дефектов', verbose_name='Выбор наличие дефектов')
    # Введите ожидания по цене
    waiting_price_message = models.TextField(default='Введите ожидания по цене', verbose_name='Введите ожидания по цене')
    # Загрузка фото №1
    photo_message_1 = models.TextField(default='Загрузка фото №1', verbose_name='Загрузка фото №1')
    # Загрузка фото №2
    photo_message_2 = models.TextField(default='Загрузка фото №2', verbose_name='Загрузка фото №2')
    # Сообщение об успешной отправки заявки
    end_message = models.TextField(default='Сообщение об успешной отправки заявки', verbose_name='Сообщение об успешной отправки заявки')
    # Консьерж текст
    concierge_message = models.TextField(default='Консьерж текст', verbose_name='Консьерж текст')
    # Ошибка заполнения
    error_applications_message = models.TextField(default='Ошибка заполнения', verbose_name='Ошибка заполнения')
    # Нет нужного бренда
    not_brand = models.TextField(default='Нет нужного бренда', verbose_name='Нет нужного бренда')
    # Не знаю. Помогите оценить
    help_to_evaluate = models.TextField(default='Не знаю. Помогите оценить', verbose_name='Не знаю. Помогите оценить')
    # Завершить загрузку фото
    end_photo_message = models.TextField(default='Завершить загрузку', verbose_name='Завершить загрузку фото')

    # Ошибка ввода почты
    error_email = models.TextField(default='Ошибка ввода почты', verbose_name='Ошибка ввода почты')
    # Ошибка ввода номера телефона
    error_phone = models.TextField(default='Ошибка ввода номера телефона', verbose_name='Ошибка ввода номера телефона')
    # Если отправили текст вместо фото
    error_photo = models.TextField(default='Текст вместо фото', verbose_name='Текст вместо фото')
    # Неудачно написал имя/фамилия
    error_name = models.TextField(default='Неудачно написал имя/фамилия', verbose_name='Неудачно написал имя/фамилия')
    # Контакт менеджера
    contact_manager = models.TextField(default='Контакт менеджера', verbose_name='Контакт менеджера')

    # Отправить сообщение ботом
    def send_telegram_message(self, chat_id, text, keyboard=None, parse_mode=None):
        bot = telepot.Bot(self.token)

        # Проверяем нужно ли отправить клавиатуру
        if keyboard is None:
            # Отправляем сообщение через бота
            try:
                bot.sendMessage(chat_id=chat_id, text=text, parse_mode=parse_mode)
            except BotWasBlockedError:
                pass
        else:
            # Отправляем сообщение через бота
            try:
                bot.sendMessage(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode=parse_mode)
            except BotWasBlockedError:
                pass

    def __str__(self):
        return self.link

    class Meta:
        verbose_name = "Настройки бота"
        verbose_name_plural = "Настройки бота"


class TelegramUser(models.Model):
    # Бот
    bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, verbose_name='Бот')
    # id
    chat_id = models.TextField(verbose_name='Чат ID')
    # Текущий шаг
    step = models.TextField(default='start_message', verbose_name='Текущий шаг')

    # Отправляем сообщение
    # Отправить пользователю сообщение
    def send_telegram_message(self, text, keyboard=None, parse_mode=None):
        if keyboard is None:
            self.bot.send_telegram_message(self.chat_id, text, parse_mode=parse_mode)
        else:
            self.bot.send_telegram_message(self.chat_id, text, keyboard, parse_mode=parse_mode)

    def __str__(self):
        return self.chat_id

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"


# Вариант категории аксессуара
class CategoryOptions(models.Model):
    # Название
    name = models.TextField(verbose_name='Название')
    # Отображать в боте
    is_visible = models.BooleanField(default=True, verbose_name='Отображать в боте')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вариант категории аксессуара"
        verbose_name_plural = "Варианты категории аксессуаров"


# Вариант бренда
class BrandOptions(models.Model):
    # Название
    name = models.TextField(verbose_name='Название')
    # Отображать в боте
    is_visible = models.BooleanField(default=True, verbose_name='Отображать в боте')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вариант бренда"
        verbose_name_plural = "Варианты брендов"


# Вариант состояния
class StateOptions(models.Model):
    # Название
    name = models.TextField(verbose_name='Название')
    # Отображать в боте
    is_visible = models.BooleanField(default=True, verbose_name='Отображать в боте')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вариант состояния"
        verbose_name_plural = "Варианты состояний"


# Вариант дефекта
class DefectOptions(models.Model):
    # Название
    name = models.TextField(verbose_name='Название')
    # Отображать в боте
    is_visible = models.BooleanField(default=True, verbose_name='Отображать в боте')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вариант дефекта"
        verbose_name_plural = "Варианты дефектов"


# Вариант сотрудничества
class CooperationOption(models.Model):
    # Название
    name = models.TextField(verbose_name='Название')
    # Отображать в боте
    is_visible = models.BooleanField(default=True, verbose_name='Отображать в боте')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вариант сотрудничества"
        verbose_name_plural = "Варианты сотрудничества"


# Заяка на продажи вещи
class SellApplication(models.Model):
    # Пользователь
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    # Статус заявки True (активная, заполняется)
    active = models.BooleanField(default=True)
    # Вариант сотрудничества
    cooperation_option = models.ForeignKey(CooperationOption, on_delete=models.CASCADE, default=None, blank=True, null=True)
    # Имя
    name = models.TextField(default=None, blank=True, null=True)
    # Почта
    email = models.TextField(default=None, blank=True, null=True)
    # Телефон
    tel = models.TextField(default=None, blank=True, null=True)
    # Категория аксессуара
    category = models.ForeignKey(CategoryOptions, on_delete=models.CASCADE, default=None, blank=True, null=True)
    # Бренд
    brand = models.ForeignKey(BrandOptions, on_delete=models.CASCADE, default=None, blank=True, null=True)
    # Модель
    model = models.TextField(default=None, blank=True, null=True)
    # Состояние
    state = models.ForeignKey(StateOptions, on_delete=models.CASCADE, default=None, blank=True, null=True)
    # Наличие дефектов
    defect = models.ForeignKey(DefectOptions, on_delete=models.CASCADE, default=None, blank=True, null=True)
    # Ожидание по цене
    waiting_price = models.FloatField(default=None, blank=True, null=True)
    # Отправил ли пользователь фото
    is_photo = models.BooleanField(default=False)
    #
    concierge_count = models.IntegerField(default=0)

    def cooperation_option_name(self):
        return self.cooperation_option.name

    def brand_name(self):
        try:
            return self.brand.name or 'не указан'
        except AttributeError:
            return 'не указан'

    def state_name(self):
        try:
            return self.state.name or 'не указано'
        except AttributeError:
            return 'не указано'

    def defect_name(self):
        try:
            return self.defect.name or 'не указано'
        except AttributeError:
            return 'не указано'

    def __str__(self):
        return self.user.chat_id

    class Meta:
        verbose_name = "Заяка продажи вещи"
        verbose_name_plural = "Заяки продажи вещей"


# Фото для заявок
class PhotoApplications(models.Model):
    # Дата отпрвки сообщения
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # Заяка
    application = models.ForeignKey(SellApplication, on_delete=models.CASCADE)
    # Фото
    photo = models.ImageField(upload_to='application_image', blank=True, null=True)

    def __str__(self):
        return self.application.user.chat_id

    class Meta:
        verbose_name = "Фото заявки"
        verbose_name_plural = "Фотографии заявки"


class AmoCRMData(models.Model):
    # Поддомен нужного аккаунта
    sub_domain = models.TextField()
    # ID интеграции
    client_id = models.TextField()
    # Секрет интеграции
    client_secret = models.TextField()
    # Полученный код авторизации
    code = models.TextField()
    # Redirect URI указанный в настройках интеграции
    redirect_uri = models.TextField()
    # Access Token в формате JWT
    access_token = models.TextField()
    # Refresh Token
    refresh_token = models.TextField()

    def __str__(self):
        return self.sub_domain

    class Meta:
        verbose_name = "Данные для AmoCRM"
        verbose_name_plural = "Данные для AmoCRM"
