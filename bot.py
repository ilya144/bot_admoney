import telebot

token = '886563861:AAHBaV1huqzmOCOmrTmfuce39MA6OC0VD10'
bot = telebot.TeleBot(token, threaded=False)

USERS = {} #СЛОВАРЬ ЮЗЕРОВ ПО ID
class User: # класс пользователя
    def __init__(self, id_, role): # role=0 executor role=1 customer
        self.id_ = id_
        self.role = role
        self.tasks = []
        self.place = [] # при нажатии на кнопку сюда закидывается название самой кнопки

# кнопка старт
@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Я Исполнитель', 'Я Заказчик')
    bot.send_message(message.from_user.id,
                     'Добро пожаловать в *Ad-Money*!\nВыберите, кто вы',
                     reply_markup=user_markup,
                     parse_mode="Markdown")


#выбор стороны - choose your destiny
@bot.message_handler(content_types=['text'])
def handle_main(message):
    #print(USERS)
    #print(message.from_user.id)

    user_id = message.from_user.id

    if message.text == 'Я Исполнитель':
        if message.from_user.id in USERS:
            USERS[user_id].role = message.text[2:]
        else:
            USERS[user_id] = User(user_id, message.text[2:])

        USERS[user_id].place = [message.text]
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Мой профиль', 'Задания')
        user_markup.row('Главное меню')
        bot.send_message(message.from_user.id,
                         'Привет, Исполнитель, выбери действие',
                         reply_markup=user_markup)

    if message.text == 'Я Заказчик':
        if message.from_user.id in USERS:
            USERS[user_id].role = message.text[2:]
        else:
            USERS[user_id] = User(user_id, message.text[2:])

        USERS[user_id].place = [message.text]
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Мой профиль', 'Баланс')
        user_markup.row('Партнерская программа')
        user_markup.row('Задания', 'Цены')
        user_markup.row('Главное меню')
        bot.send_message(message.from_user.id,
                         'Привет, Заказчик, выбери действие',
                         reply_markup=user_markup)

    if user_id in USERS:

    ######################################################################
    ###                                                                ###
    ###                   И С П О Л Н И Т Е Л Ь                        ###
    ###                                                                ###
    ######################################################################
    #                                                                    #
     ################# 1 layer after main manu executor #################

        if USERS[user_id].place[-1] == 'Я Исполнитель':
            if message.text == 'Мой профиль':
                USERS[user_id].place.append(message.text)
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('Соц сети', 'Баланс', 'Подписка')
                user_markup.row('Партнерская программа')
                user_markup.row('Назад', 'Главное меню')
                bot.send_message(message.from_user.id,
                                 'Выбери действие',
                                 reply_markup=user_markup)

            if message.text == 'Задания':
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('Инстаграм')
                user_markup.row('ВК')
                user_markup.row('Телеграм')
                user_markup.row('Назад', 'Главное меню')
                bot.send_message(message.from_user.id,
                                 'Выбери задание',
                                 reply_markup=user_markup)


    ############## END 1 layer after main manu executor END ##############

    ################## 2 layer after main manu executor ##################

    # ------------- 'Мой профиль' ---------------#
        if USERS[user_id].place[-1] == 'Мой профиль' and\
                USERS[user_id].role == 'Исполнитель':
            if message.text == 'Соц сети':
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('Инстаграм')
                user_markup.row('ВК')
                user_markup.row('Телеграм')
                user_markup.row('Назад', 'Главное меню')
                bot.send_message(message.from_user.id,
                                 'Выбери соц сеть',
                                 reply_markup=user_markup)

            if message.text == 'Баланс':

                bot.send_message(message.from_user.id,
                                 'на вашем счету: 1000000$')

            if message.text == 'Подписка':
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('Инстаграм')
                user_markup.row('ВК')
                user_markup.row('Телеграм')
                user_markup.row('Назад', 'Главное меню')
                bot.send_message(message.from_user.id,
                                 'Выбери соц сеть',
                                 reply_markup=user_markup)

            if message.text == 'Партнерская программа':
                bot.send_message(message.from_user.id,
                                 'Ваша реферальная ссылка t.me/advertmoney_bot?start=%s'%user_id)
    # -----------END 'Мой профиль' END-----------#

    # -------------- 'Задания' ---------------#
    # TODO executor Задания исполнителя
        if USERS[user_id].place[-1] == 'Задания' and\
                USERS[user_id].role == 'Исполнитель':
            pass
    # -----------END 'Задания' END------------#

    ############## END 2 layer after main manu executor END ##############


    ######################################################################
    ###                                                                ###
    ###                       З А К А З Ч И К                          ###
    ###                                                                ###
    ######################################################################
    #                                                                    #
     ################# 1 layer after main manu customer #################
    # TODO Кнопки заказчика


    ############## END 1 layer after main manu customer END ##############
    # --------------- main menu --------------#
        if message.text == 'Главное меню':
            USERS[user_id].place = []
            handle_start(message)
            return




if __name__ == "__main__":
    bot.polling()