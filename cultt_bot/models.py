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
    # Приветственное сообщение
    start_message = models.TextField(verbose_name='Приветственное сообщение')
    # Стартовая кнопка (Продать вещи)
    start_button = models.TextField(verbose_name='Стартовая кнопка')

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
    visible = models.BooleanField(default=True, validators='Отображать в боте')

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
    visible = models.BooleanField(default=True, validators='Отображать в боте')

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
    visible = models.BooleanField(default=True, validators='Отображать в боте')

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
    visible = models.BooleanField(default=True, validators='Отображать в боте')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вариант дефекта"
        verbose_name_plural = "Варианты дефектов"


# Заяка на продажи вещи
class SellApplication(models.Model):
    # Пользователь
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    # Статус заявки True (активная, заполняется)
    active = models.BooleanField(default=True)
    # Вариант сотрудничества (circulation, trade_in)
    cooperation_option = models.CharField(max_length=20, default=None, blank=True, null=True)
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

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "Заяка продажи вещи"
        verbose_name_plural = "Заяки продажи вещей"
