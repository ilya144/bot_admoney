from botmarkup import ExecutorTree, CustomerTree
from parsers import vk, instagram, telegram
from user import User
import telebot


class Bot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token, threaded=False)

        self.users = {} # key - telegram id, value - User obj

        self.message_handler(commands=["start"])(self.__start_reply)
        self.message_handler(content_types=['text'])(self.__text_reply)


    def __template_handler(self, message, reply_text, social: bool = False):
        user = self.users[message.from_user.id]

        if user.role == "Заказчик":
            markup_tree = CustomerTree
        elif user.role == "Исполнитель":
            markup_tree = ExecutorTree

        if social:
            markup = markup_tree.get_reply_markup('%s && %s' % (message.text, user.place[-1]))
        else:
            markup = markup_tree.get_reply_markup(message.text)
        user.place.append(message.text)
        self.send_message(message.from_user.id,
                          reply_text, reply_markup=markup)


    def __start_reply(self, message):
        user_id = message.from_user.id
        try:
            if int(message.text[7:]) in self.users and user_id not in self.users:
                user = self.users[int(message.text[7:])]
                user.add_ref()
        except:
            pass

        if user_id not in self.users:
            self.users[user_id] = User(user_id, None)
        else:
            self.users[user_id].place = []
            self.users[user_id].role = None

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Я Исполнитель', 'Я Заказчик')
        self.send_message(user_id,
                         'Добро пожаловать в *Ad-Money*!\nВыберите, кто вы',
                         reply_markup=user_markup,
                         parse_mode="Markdown")

    def __text_reply(self, message):
        user_id = message.from_user.id

        if user_id not in self.users:
            self.__start_reply(message)
            return
        else:
            user = self.users[user_id]

        if message.text == 'Я Исполнитель':
            user.role = message.text[2:]
            self.__template_handler(message,
                                    'Привет, Исполнитель,'
                                    ' выбери действие'
                                    )
            return

        if message.text == 'Я Заказчик':
            user.role = message.text[2:]
            self.__template_handler(message,
                                    'Привет, Заказчик,'
                                    ' выбери действие'
                                    )
            return

        if message.text == 'Главное меню':
            self.__start_reply(message)
            return

        if message.text == 'Назад':
            if len(user.place) < 2:
                return
            else:
                user.place.pop()
                message.text = user.place[-1]
                user.place.pop()
                self.__text_reply(message)
            return


        if message.text and user.role == 'Исполнитель':
            self.__executor_menu(message)
            return

        if message.text and user.role == 'Заказчик':
            self.__customer_menu(message)
            return

        if message.text == 'Партнерская программа':
            self.send_message(message.from_user.id,
                             'Ваша реферальная ссылка '
                             f't.me/advertmoney_self.start={user_id}\n'
                             f'Приглашено {user.referal} пользователей')

    def __executor_menu(self, message):
        user_id = message.from_user.id
        user = self.users[user_id]

        if message.text == 'Мой профиль' and user.place[-1] == 'Я Исполнитель':
            self.__template_handler(message, 'Выбери действие')

        if message.text == 'Задания' and user.place[-1] == 'Я Исполнитель':
            self.__template_handler(message, 'Выбери задание')

        if message.text == 'Соц сети' and user.place[-1] == 'Мой профиль':
            self.__template_handler(message, 'Выбери социальную сеть')

        if message.text == 'Баланс' and user.place[-1] == 'Мой профиль':
            self.__template_handler(message, 'Выбери действие')

        if message.text == 'Подписка' and user.place[-1] == 'Мой профиль':
            self.__template_handler(message, 'Выбери социальную сеть')

        if message.text in ('Инстаграм', 'ВК', 'Телеграм'):
            self.__template_handler(message, 'Выбери действие', social=True)

    def __customer_menu(self, message):
        user_id = message.from_user.id
        user = self.users[user_id]

        if message.text == 'Мой профиль' and user.place[-1] == 'Я Заказчик':
            self.__template_handler(message, 'Выбери действие')

        if message.text == 'Задания' and user.place[-1] == 'Я Заказчик':
            self.__template_handler(message, 'Выбери задание')

        if message.text == 'Соц сети' and user.place[-1] == 'Мой профиль':
            self.__template_handler(message, 'Выбери социальную сеть')

        if message.text == 'Баланс' and user.place[-1] == 'Я Заказчик':
            self.__template_handler(message, 'Выбери действие')

        if message.text == 'Цены' and user.place[-1] == 'Я Заказчик':
            self.__template_handler(message, 'Выбери социальную сеть')

        if message.text in ('Инстаграм', 'ВК', 'Телеграм'):
            self.__template_handler(message, 'Выбери действие', social=True)
