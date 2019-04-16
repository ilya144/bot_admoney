import telebot

token = ''
bot = telebot.TeleBot(token, threaded=False)

# кнопка старт
@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Я Исполнитель', 'Я Заказчик')
    bot.send_message(message.from_user.id,
                     'Добро пожаловать в *Ad-Money*!\nВыберите, кто вы',
                     reply_markup=user_markup,
                     parse_mode="Markdown")

#выбор стороны - choose your destiny))
@bot.message_handler(content_types=['text'])
def handle_main(message):
    if message == 'Я Исполнитель':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Мой профиль', 'Задания')
        user_markup.row('Главное меню')
        bot.send_message(message.from_user.id,
                         'Привет, Исполнитель, выбери действие',
                         reply_markup=user_markup)

    if message == 'Я Заказчик':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Мой профиль', 'Баланс')
        user_markup.row('Партнерская программа')
        user_markup.row('Задания', 'Цены')
        user_markup.row('Главное меню')
        bot.send_message(message.from_user.id,
                         'Привет, Заказчик, выбери действие',
                         reply_markup=user_markup)

# меню исполнителя
@bot.message_handler(content_types=['text'])
def handle_executor(message):
    pass

# меню заказчика
@bot.message_handler(content_types=['text'])
def handle_customer(message):
    pass



if __name__ == "__main__":
    bot.polling()