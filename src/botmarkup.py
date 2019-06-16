import telebot

class MarkupTree:

    @staticmethod
    def __reply_markup(buttons: list) -> telebot.types.ReplyKeyboardMarkup:
        " buttons looks like [[one, two],[one_on_next_row, ...], ...]"
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for row in buttons:
            if type(row) == str:
                markup.row(row)
            else:
                markup.row(*row)
        return markup

    @staticmethod
    def __inline_markup(buttons: list) -> telebot.types.InlineKeyboardMarkup:
        " buttons looks like [[one, two],[one_on_next_row, ...], ...]"
        markup = telebot.types.InlineKeyboardMarkup()
        new_buttons = []
        for row in buttons:
            new_row = []
            for button in row:
                but_obj = telebot.types.InlineKeyboardButton(**button)
                new_row.append(but_obj)
            new_buttons.append(new_row)
        for row in new_buttons:
            markup.row(*row)
        return markup

    @classmethod
    def get_reply_markup(cls, button_name: str) -> telebot.types.ReplyKeyboardMarkup:
        buttons = cls.markup_dict[button_name]
        markup = cls.__reply_markup(buttons)
        return markup

    @classmethod
    def get_inline_markup(cls, button_name: str) -> telebot.types.InlineKeyboardMarkup:
        buttons = cls.markup_dict[button_name]
        markup = cls.__inline_markup(buttons)
        return markup


######################################################################
###                                                                ###
###                   И С П О Л Н И Т Е Л Ь                        ###
###                                                                ###
######################################################################

class ExecutorTree(MarkupTree):
    # -- reply --

    main = [
        ('Мой профиль', 'Задания'),
        ('Главное меню')
    ]

    my_profile = [
        ('Соц сети', 'Баланс', 'Подписка'),
        ('Партнерская программа'),
        ('Назад', 'Главное меню')
    ]

    tasks = [
        ('Инстаграм'),
        ('ВК'),
        ('Телеграм'),
        ('Назад', 'Главное меню')
    ]

    social_media = tasks[:]

    balance = [
        ('Статистика', 'Вывод средств'),
        ('Назад', 'Главное меню')
    ]
    # -- inline -- but not yet by now

    subscribe = [
        (
            {"text": 'Инстаграм',
             "callback_data": "Подписка-Инстаграм"},
            {"text": 'ВК',
             "callback_data": "Подписка-ВК"},
            {"text": 'Телеграм',
             "callback_data": "Подписка-Телеграм"}
         ),
        (
            {"text": 'Подписаться на всё',
             "callback_data": "Подписка-7"},
            {"text": 'Отписаться от всех заданий',
             "callback_data": "Подписка-0"}
         )
    ]

    instagram_settings = [
        ('Изменить ник', 'Назад')
    ]

    vk_settings = [
        ('Изменить ID или ник', 'Назад')
    ]

    telegram_settings = [
        ('Подтвердите, что вы не бот'),
        ('Назад')
    ]

    instagram_tasks = [
        ('Поставить лайк', 'Подписаться'),
        ('Прокомментировать'),
        ('Назад', 'Главное меню')
    ]

    vk_tasks = [
        ('Поставить лайк', 'Подписаться'),
        ('Прокомментировать', 'Зарепостить'),
        ('Назад', 'Главное меню')
    ]

    telegram_tasks = [
        ('Подписаться', 'Посмотреть пост'),
        ('Назад', 'Главное меню')
    ]

    markup_dict = {
        'Я Исполнитель': main,
        'Мой профиль': my_profile,
        'Задания': tasks,
        'Соц сети': social_media,
        'Баланс': balance,
        'Подписка': subscribe,
        'Инстаграм && Соц сети': instagram_settings,
        'ВК && Соц сети': vk_settings,
        'Телеграм && Соц сети': telegram_settings,
        'Инстаграм && Задания': instagram_tasks,
        'ВК && Задания': vk_tasks,
        'Телеграм && Задания': telegram_tasks,
    }


######################################################################
###                                                                ###
###                       З А К А З Ч И К                          ###
###                                                                ###
######################################################################

class CustomerTree(MarkupTree):

    main = [
        ('Мой профиль', 'Баланс'),
        ('Партнерская программа'),
        ('Задания', 'Цены'),
        ('Главное меню')
    ]

    my_profile = [
        ('Соц сети'),
        ('Назад', 'Главное меню')
    ]

    tasks = [
        ('Инстаграм'),
        ('ВК'),
        ('Телеграм'),
        ('Назад', 'Главное меню')
    ]

    social_media = tasks[:]

    balance = [
        ('Пополнить баланс'),
        ('Статистика'),
        ('Назад', 'Главное меню')
    ]

    prices = [
        (
            {"text": 'Инстаграм',
             "callback_data": "Цены-Инстаграм"},
            {"text": 'ВК',
             "callback_data": "Цены-ВК"},
            {"text": 'Телеграм',
             "callback_data": "Цены-Телеграм"}
         )
    ]

    instagram_settings = [
        ('Изменить ник', 'Назад')
    ]

    vk_settings = [
        ('Ввести ID или ник', 'Назад')
    ]

    telegram_settings = [
        ('Подтвердите, что вы не бот'),
        ('Назад')
    ]

    instagram_tasks = [
        ('Поставить лайк', 'Подписаться'),
        ('Прокомментировать'),
        ('Назад', 'Главное меню')
    ]

    vk_tasks = [
        ('Поставить лайк', 'Подписаться'),
        ('Прокомментировать', 'Зарепостить'),
        ('Назад', 'Главное меню')
    ]

    telegram_tasks = [
        ('Подписаться', 'Посмотреть пост'),
        ('Назад', 'Главное меню')
    ]

    markup_dict = {
        'Я Заказчик': main,
        'Мой профиль': my_profile,
        'Задания': tasks,
        'Соц сети': social_media,
        'Баланс': balance,
        'Цены': prices,
        'Инстаграм && Соц сети': instagram_settings,
        'ВК && Соц сети': vk_settings,
        'Телеграм && Соц сети': telegram_settings,
        'Инстаграм && Задания': instagram_tasks,
        'ВК && Задания': vk_tasks,
        'Телеграм && Задания': telegram_tasks,
    }
