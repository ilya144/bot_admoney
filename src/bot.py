# TODO del all, cause this is actually shit
#
#
#

import telebot
from db_client import Database
from botmarkup import ExecutorTree, CustomerTree
from parsers import vk, instagram, telegram


token = '886563861:AAHBaV1huqzmOCOmrTmfuce39MA6OC0VD10'
bot = telebot.TeleBot(token, threaded=False)

self.users = {} #dict of self.users, key is the user id
class User(Database):
    def __init__(self, id_, role):
        """
        bot self.users class, inherit from Database

        :param id_: equals Telegram user id
        :param role: may be Заказчик or Исполнитель, None in main menu
        """
        self.id_ = id_
        self.role = role
        self.tasks = []
        self.place = [] # onclick button append button name to that list
        self.referal = 0 # number of invited self.users
        # TODO db_inteface, could be an inheritance
        # !!! I MOVE IT TO user.py
        # TODO del




@bot.message_handler(commands=["start"])# /start command and button
def handle_start(message):
    user_id = message.from_user.id
    try:
        if int(message.text[7:]) in self.users and user_id not in self.users:
            u = self.users[int(message.text[7:])]
            u.referal+=1
            #db.update_user(u.ID, u.activedays, u.get_accs(),u.referal)
    except: pass
    if user_id not in self.users:
        self.users[user_id] = User(user_id, None)
        try:
            self.users_db.insert_user(user_id, 0, 0)
        except:
            # TODO fetching user data from db
            pass
    else:
        self.users[user_id].place = []
        self.users[user_id].role = None

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Я Исполнитель', 'Я Заказчик')
    bot.send_message(message.from_user.id,
                     'Добро пожаловать в *Ad-Money*!\nВыберите, кто вы',
                     reply_markup=user_markup,
                     parse_mode="Markdown")


@bot.message_handler(content_types=['text'])# choose your destiny
def handle_main(message):
    user_id = message.from_user.id

    if user_id not in self.users:
        handle_start(message)
        return
    else:
        user = self.users[user_id]

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


def handle_executor(message):
    user_id = message.from_user.id
    user = self.users[user_id]
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
    user = self.users[user_id]
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

# TODO del
# def vk_change_id(message):
#     username = message.text.split("vk.com")[1].strip("/")
#     vk_id = vkparser._get_user_id(username)
#     self.users_db.update_user(message.from_user.id, _vk_id=vk_id)
#
# def insta_change_id(message):
#     username = message.text.split("instagram.com")[1].strip("/")
#     insta_id = instaparser._get_id_by_username(username)
#     self.users_db.update_user(message.from_user.id, _insta_id=insta_id)


if __name__ == "__main__":
    self.users_db = Database("self.users.db")
    #vkparser = vk.VKParser()
    #instaparser = instagram.InstagramParser()
    bot.polling(none_stop=True)
