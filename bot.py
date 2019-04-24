import telebot
from botmarkup import ExecutorTree, CustomerTree

token = '886563861:AAHBaV1huqzmOCOmrTmfuce39MA6OC0VD10'
bot = telebot.TeleBot(token, threaded=False)

USERS = {} #dict of users, key is the user id
class User:
    def __init__(self, id_, role):
        """
        bot users class

        :param id_: equals Telegram user id
        :param role: may be Заказчик, Исполнитель, None in main menu
        """
        self.id_ = id_
        self.role = role
        self.tasks = []
        self.place = [] # onclick button append button name to that list
        self.referal = 0 # number of invited users


@bot.message_handler(commands=["start"])# /start command and button
def handle_start(message):
    user_id = message.from_user.id
    try:
        if int(message.text[7:]) in USERS and user_id not in USERS:
            u = USERS[int(message.text[7:])]
            u.referal+=1
            #db.update_user(u.ID, u.activedays, u.get_accs(),u.referal)
    except: pass
    if user_id not in USERS:
        USERS[user_id] = User(user_id, None)
    else:
        USERS[user_id].place = []
        USERS[user_id].role = None

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Я Исполнитель', 'Я Заказчик')
    bot.send_message(message.from_user.id,
                     'Добро пожаловать в *Ad-Money*!\nВыберите, кто вы',
                     reply_markup=user_markup,
                     parse_mode="Markdown")


@bot.message_handler(content_types=['text'])# choose your destiny
def handle_main(message):
    user_id = message.from_user.id

    if user_id not in USERS:
        handle_start(message)
        return
    else:
        user = USERS[user_id]

    if message.text == 'Я Исполнитель':

        user.role = message.text[2:]
        user.place = [message.text]

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Мой профиль', 'Задания')
        user_markup.row('Главное меню')
        bot.send_message(message.from_user.id,
                         'Привет, Исполнитель, выбери действие',
                         reply_markup=user_markup)
        return

    if message.text == 'Я Заказчик':

        user.role = message.text[2:]
        user.place = [message.text]

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Мой профиль', 'Баланс')
        user_markup.row('Партнерская программа')
        user_markup.row('Задания', 'Цены')
        user_markup.row('Главное меню')
        bot.send_message(message.from_user.id,
                         'Привет, Заказчик, выбери действие',
                         reply_markup=user_markup)
        return

    if message.text == 'Главное меню':
        handle_start(message)
        return

    if message.text == 'Партнерская программа':
        bot.send_message(message.from_user.id,
                         f'Ваша реферальная ссылка t.me/advertmoney_bot?start={user_id}\n'
                         f'Приглашено {user.referal} пользователей')

    if message.text == 'Назад':
        if len(user.place)<2:
            return
        else:
            user.place.pop()
            message.text = user.place[-1]
            user.place.pop()
            handle_main(message)
        return


    if message.text and user.role == 'Исполнитель':
        handle_executor(message)
        return

    if message.text and user.role == 'Заказчик':
        handle_customer(message)
        return


#def handlers(message, user_id, USERS):
def handle_executor(message):
    user_id = message.from_user.id
    user = USERS[user_id]
    markup_tree = ExecutorTree()

    if message.text == "Мой профиль" and user.place[-1] == 'Я Исполнитель':
        markup = markup_tree.get_reply_markup(message.text)
        user.place.append(message.text)
        bot.send_message(message.from_user.id,
                         'Выбери действие',
                         reply_markup=markup)

    if message.text == 'Задания' and user.place[-1] == 'Я Исполнитель':
        markup = markup_tree.get_reply_markup(button_name=message.text)
        user.place.append(message.text)
        bot.send_message(message.from_user.id,
                         'Выбери задание',
                         reply_markup=markup)

    if message.text == 'Соц сети' and user.place[-1] == 'Мой профиль':
        markup = markup_tree.get_reply_markup(message.text)
        user.place.append(message.text)
        bot.send_message(message.from_user.id,
                         'Выбери социальную сеть',
                         reply_markup=markup)

    if message.text == 'Баланс' and user.place[-1] == 'Мой профиль':
        markup = markup_tree.get_reply_markup(message.text)
        user.place.append(message.text)
        bot.send_message(message.from_user.id,
                         'Выбери действие',
                         reply_markup=markup)

    if message.text == 'Подписка' and user.place[-1] == 'Мой профиль':
        markup = markup_tree.get_reply_markup(message.text)
        user.place.append(message.text)
        bot.send_message(message.from_user.id,
                         'Выбери социальную сеть',
                         reply_markup=markup)

    if message.text in ('Инстаграм', 'ВК', 'Телеграм'):
        if user.place[-1] == 'Соц сети':
            markup = markup_tree.get_reply_markup('%s && %s'%(message.text, 'Соц сети'))
            user.place.append(message.text)
            bot.send_message(message.from_user.id,
                             'Выбери действие',
                             reply_markup=markup)
        elif user.place[-1] == 'Задания':
            markup = markup_tree.get_reply_markup('%s && %s' % (message.text, 'Задания'))
            user.place.append(message.text)
            bot.send_message(message.from_user.id,
                             'Выбери действие',
                             reply_markup=markup)

def handle_customer(message):
    user_id = message.from_user.id
    user = USERS[user_id]
    markup_tree = CustomerTree()

    if message.text == 'Мой профиль' and user.place[-1] == 'Я Заказчик':
        markup = markup_tree.get_reply_markup(message.text)
        user.place.append(message.text)
        bot.send_message(message.from_user.id,
                         'Выбери действие',
                         reply_markup=markup)

    if message.text == 'Задания' and user.place[-1] == 'Я Заказчик':
        markup = markup_tree.get_reply_markup(button_name=message.text)
        user.place.append(message.text)
        bot.send_message(message.from_user.id,
                         'Выбери задание',
                         reply_markup=markup)

    if message.text == 'Соц сети' and user.place[-1] == 'Мой профиль':
        markup = markup_tree.get_reply_markup(message.text)
        user.place.append(message.text)
        bot.send_message(message.from_user.id,
                         'Выбери социальную сеть',
                         reply_markup=markup)

    if message.text == 'Баланс' and user.place[-1] == 'Я Заказчик':
        markup = markup_tree.get_reply_markup(message.text)
        user.place.append(message.text)
        bot.send_message(message.from_user.id,
                         'Выбери действие',
                         reply_markup=markup)

    if message.text == 'Цены' and user.place[-1] == 'Я Заказчик':
        markup = markup_tree.get_reply_markup(message.text)
        user.place.append(message.text)
        bot.send_message(message.from_user.id,
                         'Выбери социальную сеть',
                         reply_markup=markup)

    if message.text in ('Инстаграм', 'ВК', 'Телеграм'):
        if user.place[-1] == 'Соц сети':
            markup = markup_tree.get_reply_markup('%s && %s'%(message.text, 'Соц сети'))
            user.place.append(message.text)
            bot.send_message(message.from_user.id,
                             'Выбери действие',
                             reply_markup=markup)
        elif user.place[-1] == 'Задания':
            markup = markup_tree.get_reply_markup('%s && %s' % (message.text, 'Задания'))
            user.place.append(message.text)
            bot.send_message(message.from_user.id,
                             'Выбери действие',
                             reply_markup=markup)


class InstagramParser:
    def __init__(self):
        pass

    def get_like(self):
        pass

    def get_comment(self):
        pass

    def get_follower(self):
        pass


class VKParser:
    def __init__(self):
        pass

    def get_like(self):
        pass

    def get_comment(self):
        pass

    def get_follower(self):
        pass

class TelegramParser:
    def __init__(self):
        pass

    def get_follower(self):
        pass


if __name__ == "__main__":
    bot.polling(none_stop=True)