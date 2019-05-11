import telebot

######################################################################
###                                                                ###
###                   И С П О Л Н И Т Е Л Ь                        ###
###                                                                ###
######################################################################

class ExecutorTree:
    # -- reply --
    # u'Мой профиль'
    my_profile = [
        ('Соц сети', 'Баланс', 'Подписка'),
        ('Партнерская программа'),
        ('Назад', 'Главное меню')
    ]
    # u'Задания'
    tasks = [
        ('Инстаграм'),
        ('ВК'),
        ('Телеграм'),
        ('Назад', 'Главное меню')
    ]
    # u'Соц сети'
    social_media = tasks[:]
    # u'Баланс'
    balance = [
        ('Статистика', 'Вывод средств'),
        ('Назад', 'Главное меню')
    ]
    # -- inline -- but not yet by now
    # u'Подписка'
    subscribe = [
        ('Инстаграм', 'ВК', 'Телеграм'),
        ('Назад', 'Главное меню')
    ]
    # u'Инстаграм' set
    instagram_settings = [
        ('Ввести ник', 'Поменять ник'),
        ('Назад', 'Главное меню')
    ]
    # u'ВК' set
    vk_settings = [
        ('Ввести ID или ник', 'Поменять ID или ник'),
        ('Назад', 'Главное меню')
    ]
    # u'Телеграм' set
    telegram_settings = [
        ('Подтвердите, что вы не бот'),
        ('Назад', 'Главное меню')
    ]
    # u'Инстаграм' task
    instagram_tasks = [
        ('Поставить лайк', 'Подписаться'),
        ('Прокомментировать'),
        ('Назад', 'Главное меню')
    ]
    # u'ВК' task
    vk_tasks = [
        ('Поставить лайк', 'Подписаться'),
        ('Прокомментировать', 'Зарепостить'),
        ('Назад', 'Главное меню')
    ]
    # u'Телеграм' task
    telegram_tasks = [
        ('Подписаться', 'Посмотреть пост'),
        ('Назад', 'Главное меню')
    ]

    markup_dict = {
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
    def _reply_markup(self, buttons: list) -> telebot.types.ReplyKeyboardMarkup:
        " buttons looks like [[one, two],[one_on_next_row, ...], ...]"
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for row in buttons:
            if type(row) == str:
                markup.row(row)
            else:
                markup.row(*row)
        return markup

    def _inline_markup(self, buttons: list) -> telebot.types.InlineKeyboardMarkup:
        " buttons looks like [[one, two],[one_on_next_row, ...], ...]"
        markup = telebot.types.InlineKeyboardMarkup()
        for row in buttons:
            if type(row) == str:
                markup.row(row)
            else:
                markup.row(*row)
        return markup

    def get_reply_markup(self, button_name: str) -> telebot.types.ReplyKeyboardMarkup:
        buttons = self.markup_dict[button_name]
        markup = self._reply_markup(buttons)
        return markup

    def get_inline_markup(self, button_name: str) -> telebot.types.InlineKeyboardMarkup:
        buttons = self.markup_dict[button_name]
        markup = self._inline_markup(buttons)
        return markup


######################################################################
###                                                                ###
###                       З А К А З Ч И К                          ###
###                                                                ###
######################################################################

class CustomerTree:

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
        ('Инстаграм', 'ВК', 'Телеграм'),
        ('Назад', 'Главное меню')
    ]
    # u'Инстаграм' set
    instagram_settings = [
        ('Ввести ник', 'Поменять ник'),
        ('Назад', 'Главное меню')
    ]
    # u'ВК' set
    vk_settings = [
        ('Ввести ID или ник', 'Поменять ID или ник'),
        ('Назад', 'Главное меню')
    ]
    # u'Телеграм' set
    telegram_settings = [
        ('Подтвердите, что вы не бот'),
        ('Назад', 'Главное меню')
    ]
    # u'Инстаграм' task
    instagram_tasks = [
        ('Поставить лайк', 'Подписаться'),
        ('Прокомментировать'),
        ('Назад', 'Главное меню')
    ]
    # u'ВК' task
    vk_tasks = [
        ('Поставить лайк', 'Подписаться'),
        ('Прокомментировать', 'Зарепостить'),
        ('Назад', 'Главное меню')
    ]
    # u'Телеграм' task
    telegram_tasks = [
        ('Подписаться', 'Посмотреть пост'),
        ('Назад', 'Главное меню')
    ]

    markup_dict = {
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

    def _reply_markup(self, buttons: list) -> telebot.types.ReplyKeyboardMarkup:
        " buttons looks like [[one, two],[one_on_next_row, ...], ...]"
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for row in buttons:
            if type(row) == str:
                markup.row(row)
            else:
                markup.row(*row)
        return markup

    def _inline_markup(self, buttons: list) -> telebot.types.InlineKeyboardMarkup:
        " buttons looks like [[one, two],[one_on_next_row, ...], ...]"
        markup = telebot.types.InlineKeyboardMarkup()
        for row in buttons:
            if type(row) == str:
                markup.row(row)
            else:
                markup.row(*row)
        return markup

    def get_reply_markup(self, button_name: str) -> telebot.types.ReplyKeyboardMarkup:
        buttons = self.markup_dict[button_name]
        markup = self._reply_markup(buttons)
        return markup

    def get_inline_markup(self, button_name: str) -> telebot.types.InlineKeyboardMarkup:
        buttons = self.markup_dict[button_name]
        markup = self._inline_markup(buttons)
        return markup


