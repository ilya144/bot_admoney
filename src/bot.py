from botmarkup import ExecutorTree, CustomerTree, OtherTree
from parsers import vk, instagram, telegram
from user import User
import telebot


class Bot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token, threaded=False)

        self.users = {} # key - telegram id, value - User obj

        self.message_handler(commands=["start"]
                             )(self.__start_reply)

        self.message_handler(content_types=['text']
                             )(self.__text_reply)

        self.callback_query_handler(func=lambda call: True
                                    )(self.__query_inline)

        self.task_tuple = ('Зарепостить', 'Посмотреть пост', 'Подписаться',
                      'Прокомментировать', 'Поставить лайк')


    def __template_handler(self, message, reply_text,
                           social: bool = False, inline: bool = False, parse_mode=None):
        user = self.users[message.from_user.id]

        if user.role == "Заказчик":
            markup_tree = CustomerTree
        elif user.role == "Исполнитель":
            markup_tree = ExecutorTree

        if not inline:
            if social:
                markup = markup_tree.get_reply_markup('%s && %s' % (message.text,
                                                                    user.place[-1])
                                                      )
            else:
                markup = markup_tree.get_reply_markup(message.text)
            user.place.append(message.text)
        else:
            markup = markup_tree.get_inline_markup(message.text)
        self.send_message(message.from_user.id,
                          reply_text,
                          reply_markup=markup,
                          parse_mode=parse_mode)


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
                         'Добро пожаловать в *SMM-TARGET*!\nВыберите, кто вы',
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

        if message.text == 'Партнерская программа':
            self.send_message(message.from_user.id,
                             'Ваша реферальная ссылка:\n'
                             f't.me/advertmoney_self.start={user_id}\n'
                             f'Приглашено {user.referal} пользователей\n\n'
                             'Вы <b>получите</b> 20% от всех покупок\n'
                             'и 30% от прибыли привлеченных\n'
                             'пользователей', parse_mode="html")

        if message.text and user.role == 'Исполнитель':
            self.__executor_menu(message)
            return

        if message.text and user.role == 'Заказчик':
            self.__customer_menu(message)
            return

    def __social_networks(self, message, user):
        if message.text == 'Соц сети' and user.place[-1] == 'Мой профиль':
            insta_acc = "Отсутствует" if user.insta_id == None else user.insta_id
            vk_acc = "Отсутствует" if user.vk_id == None else user.vk_id
            self.__template_handler(message,
                                    'Аккаунты в соц сетях:\n'
                                    f'Инстаграм: {insta_acc},\n'
                                    f'ВК: {vk_acc},\n'
                                    f'Телеграм: {user.user_id},\n'
                                    f'Выберите соц сеть для настройки')


    def __social_change(self, message, user):
        if message.text == 'Изменить ник' and user.place[-1] == 'Инстаграм':
            msg = self.send_message(message.chat.id,
                                   'Введите ник',
                                   reply_markup=self.input_markup)
            self.register_next_step_handler(msg, self.__change_instagram)

        if message.text == 'Изменить ID или ник' and user.place[-1] == 'ВК':
            msg = self.send_message(message.chat.id,
                                   'Введите ID или ник',
                                   reply_markup=self.input_markup)
            self.register_next_step_handler(msg, self.__change_vk)

        if message.text == 'Подтвердите, что вы не бот' and user.place[-1] == 'Телеграм':
            self.send_message(message.chat.id, 'Аккаунт подтвержден')

    def __change_instagram(self, message):
        user_id = message.from_user.id
        user = self.users[user_id]
        if message.text == 'Отмена':
            message.text = user.place.pop()
            self.__text_reply(message)
            return
        else:
            insta_parser = instagram.InstagramParser()
            if insta_parser.check_username(message.text):
                user.change_insta_id(message.text)
                self.send_message(message.chat.id,'Аккаунт добавлен')
            else:
                self.send_message(message.chat.id,'Аккаунт не найден')
            message.text = user.place.pop()
            self.__text_reply(message)
            return


    def __change_vk(self, message):
        user_id = message.from_user.id
        user = self.users[user_id]
        if message.text == 'Отмена':
            message.text = user.place.pop()
            self.__text_reply(message)
            return
        else:
            try:
                vkparser = vk.VKParser()
                vk_id = vkparser.check_username(message.text)
                user.change_vk_id(message.text)
                self.send_message(message.chat.id,'Аккаунт добавлен')
            except Exception as e:
                print(str(e))
                self.send_message(message.chat.id,'Аккаунт не найден')
            message.text = user.place.pop()
            self.__text_reply(message)
            return

    def __task_choice(self, message, user):

        if message.text in self.task_tuple:
            if user.role == "Заказчик":
                self.__task_creation(message, user)
            elif user.role == "Исполнитель":
                self.__task_list(message, user)

    def __task_creation(self, message, user):
        task = {}
        if user.place[-1] in ('Инстаграм', 'ВК', 'Телеграм'):
            task['task_social'] = user.place[-1]

        if message.text in self.task_tuple:task['task_name'] = message.text
        else: return

        msg = self.send_message(message.chat.id,
                                "Введите количество действий\n"
                                "(лайков, подписок и т.д.)",
                                reply_markup=OtherTree.input_markup)
        self.register_next_step_handler(msg,
                                        lambda message:
                                        self.__task_actions(message,
                                                            task,
                                                            user)
                                        )

    def __task_actions(self, message, task: dict, user):
        if message.text == 'Отмена':
            message.text = user.place.pop()
            self.__text_reply(message)
            return
        try:
            task['actions'] = int(message.text)
        except:
            # TODO task actions validation
            pass

        if task['task_name'] == "Подписаться":
            if task['task_social'] == "Инстаграм":
                task['task_obj'] = "пользователя"
            else:
                task['task_obj'] = "группу"
        else:
            task['task_obj'] = "пост"

        msg = self.send_message(message.chat.id,
                                f"Введите ссылку на {task['task_obj']} "
                                "в формате social.com/object_id "
                                "(без проблеов)",
                                reply_markup=OtherTree.input_markup)

        self.register_next_step_handler(msg,
                                        lambda message:
                                        self.__task_link(message,
                                                         task,
                                                         user)
                                        )

    def __task_link(self, message, task: dict, user):
        if message.text == 'Отмена':
            message.text = user.place.pop()
            self.__text_reply(message)
            return
        # TODO task link validation
        link = message.text.lstrip('https://www.')
        task['task_link'] = message.text
        user.add_task(**task)
        self.send_message(message.chat.id,
                          "Задание успешно добавлено")
        message.text = user.place.pop()
        self.__text_reply(message)
        return

    def __task_confirm(self, message, task: dict, user):
        self.send_message(message.chat.id,
                          "Подтвердите задание",
                          #TODO confirm task message text
                          reply_markup=OtherTree.confirm_markup)

    def __task_list(self, message, user):
        tasks = user.fetch_tasks_by_attr(user.place[-1], message.text)
        if tasks == []:
            self.send_message(user.user_id, "Заданий нет")
        else:
            for task in tasks:
                self.send_message(user.user_id,
                                  f"Задание #{task[0]}\n"
                                  f"Социальная сеть: {task[3]}\n"
                                  f"Задание: {task[4]}\n"
                                  f"Ссылка: {task[5]}\n")


    def __task_accept(self, message, user):
        pass

    #def __task_


    def __executor_menu(self, message):
        user_id = message.from_user.id
        user = self.users[user_id]

        if message.text == 'Мой профиль' and user.place[-1] == 'Я Исполнитель':
            self.__template_handler(message, 'Выбери действие')

        if message.text == 'Задания' and user.place[-1] == 'Я Исполнитель':
            self.__template_handler(message, 'Выбери задание')
            # TODO making tasks

        if message.text == 'Баланс' and user.place[-1] == 'Мой профиль':
            self.__template_handler(message, 'Выбери действие')
            # TODO inline menu with payment

        if message.text == 'Подписка' and user.place[-1] == 'Мой профиль':
            bin_subs = list(bin(user.subscribe)[2:])
            while len(bin_subs)<3:bin_subs.insert(0,0)
            inst_sub, vk_sub, tg_sub = list(map(lambda x:
                                                "Включена" if bool(int(x))
                                                else
                                                "Отключена",
                                                bin_subs))
            self.__template_handler(message,
                                    'Подписка на задания по соц сетям:\n'
                                    f'<b>Инстаграм</b>: {inst_sub},\n'
                                    f'<b>ВК</b>: {vk_sub},\n'
                                    f'<b>Телеграм</b>: {tg_sub},\n',
                                    inline=True,
                                    parse_mode="html")


        if message.text in ('Инстаграм', 'ВК', 'Телеграм'):
            self.__template_handler(message, 'Выбери действие', social=True)

        self.__social_networks(message, user)
        self.__social_change(message, user)
        self.__task_choice(message, user)


    def __customer_menu(self, message):
        user_id = message.from_user.id
        user = self.users[user_id]

        if message.text == 'Мой профиль' and user.place[-1] == 'Я Заказчик':
            self.__template_handler(message, 'Выбери действие')

        if message.text == 'Задания' and user.place[-1] == 'Я Заказчик':
            self.__template_handler(message, 'Выбери задание')

        if message.text == 'Баланс' and user.place[-1] == 'Я Заказчик':
            self.__template_handler(message, 'Выбери действие')
            # TODO same showing money and payment

        if message.text == 'Цены' and user.place[-1] == 'Я Заказчик':
            self.__template_handler(message,
                                    'Для какой соц сети показать цены?',
                                    inline=True)

        if message.text in ('Инстаграм', 'ВК', 'Телеграм'):
            self.__template_handler(message, 'Выбери действие', social=True)

        self.__social_networks(message, user)
        self.__social_change(message, user)
        self.__task_choice(message, user)



    def __query_inline(self, call):
        user_id = call.message.chat.id

        if user_id not in self.users:
            self.__start_reply(call.message)
            return
        else:
            user = self.users[user_id]

        if 'Цены' in call.data:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(telebot.types.InlineKeyboardButton(
                text="Назад", callback_data='Назад-Цены'))
            if call.data == 'Назад-Цены':
                self.edit_message_text(chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       text="Для какой соц сети показать цены?")
                keyboard = CustomerTree.get_inline_markup("Цены")

            elif call.data == 'Цены-Инстаграм':
                self.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="Действие\tЗаказчик\tИсполнитель\n"
                                           "Подписаться:\t 1 \t 0.4 рублей\n"
                                           "Поставить лайк:\t 0.5 \t 0.2 рублей\n"
                                           "Оставить комментарий:\t 3 \t 1 рублей\n")
            elif call.data == 'Цены-ВК':
                self.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="Действие\tЗаказчик\tИсполнитель\n"
                                           "Вступить в группу:\t 1 \t 0.4 рублей\n"
                                           "Поставить лайк:\t 0.5 \t 0.2 рублей\n"
                                           "Оставить комментарий:\t 3 \t 1 рублей\n"
                                           "Поделиться записью:\t 1 \t 0.4 \n")
            elif call.data == 'Цены-Телеграм':
                self.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="Действие\tЗаказчик\tИсполнитель\n"
                                           "Подписаться на канал:\t 1 \t 0.4 рублей\n"
                                           "Поставить лайк:\t 0.3 \t 0.1\n")
            self.edit_message_reply_markup(chat_id=call.message.chat.id,
                                           message_id=call.message.message_id,
                                           reply_markup=keyboard)

        if 'Подписка' in call.data:
            old_sub = user.subscribe
            if call.data == 'Подписка-Инстаграм':
                new_sub = old_sub - 4 if old_sub & 4 else old_sub + 4

            elif call.data == 'Подписка-ВК':
                new_sub = old_sub - 2 if old_sub & 2 else old_sub + 2

            elif call.data == 'Подписка-Телеграм':
                new_sub = old_sub - 1 if old_sub & 1 else old_sub + 1

            elif call.data == 'Подписка-7':
                new_sub = 7

            elif call.data == 'Подписка-0':
                new_sub = 0

            if (new_sub == old_sub):
                return

            user.change_subscribe(new_sub)

            bin_subs = list(bin(user.subscribe)[2:])
            while len(bin_subs) < 3: bin_subs.insert(0, 0)
            inst_sub, vk_sub, tg_sub = list(map(lambda x:
                                                "Включена" if bool(int(x))
                                                else
                                                "Отключена",
                                                bin_subs))

            self.edit_message_text(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   text='Подписка на задания по соц сетям:\n'
                                        f'<b>Инстаграм</b>: {inst_sub},\n'
                                        f'<b>ВК</b>: {vk_sub},\n'
                                        f'<b>Телеграм</b>: {tg_sub},\n',
                                   parse_mode="html",
                                   reply_markup=ExecutorTree.get_inline_markup("Подписка"))


        if call.data == 'Оплата':

            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(telebot.types.InlineKeyboardButton(
                    text="Банковская карта", callback_data='CreditCard'))
            keyboard.add(telebot.types.InlineKeyboardButton(
                    text="Яндекс деньги", callback_data='YandexMoney'))
            keyboard.add(telebot.types.InlineKeyboardButton(
                    text="Qiwi", callback_data='Qiwi'))
            keyboard.add(telebot.types.InlineKeyboardButton(
                    text="PayPal", callback_data='PayPal'))
            keyboard.add(telebot.types.InlineKeyboardButton(
                    text="Биткоины", callback_data='Bitcoin'))
            keyboard.add(telebot.types.InlineKeyboardButton(
                    text="Назад", callback_data='To Ref'))
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Выберите способ оплаты")
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=keyboard)
