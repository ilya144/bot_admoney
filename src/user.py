from db_client import Database
from random import randint


class User(Database):
    def __sync_db(self):
        current_user = self.fetch_user_by_id(self.user_id)

        if current_user == None:
            self.insert_user(self.user_id,
                             self.referal,
                             self.money)
        else:
            self.user_id,\
            self.vk_id,\
            self.insta_id,\
            self.referal,\
            self.money,\
            self.subscribe = current_user

    def __save_user(self):
        self.update_user(self.user_id,
                         vk_id = self.vk_id,
                         insta_id = self.insta_id,
                         referal = self.referal,
                         money = self.money,
                         subscribe = self.subscribe)


    def __init__(self, user_id, role=None):
        """
        bot users class, inherited from Database interface

        :param user_id: equals Telegram user id
        :param role: may be Заказчик or Исполнитель, None in main menu
        """
        super().__init__("Bot.db")

        self.user_id = user_id # Telegram id
        self.vk_id = None
        self.insta_id = None

        self.referal = 0  # number of invited users
        self.money = 0 # rub
        self.subscribe = 0 # 0 no one sub, 7 - vk, insta, telegram

        self.role = role
        self.tasks = []
        self.place = [] # onclick append name of button to list

        self.__sync_db()


    def add_ref(self):
        self.referal+=1
        self.__save_user()

    def change_vk_id(self, vk_id):
        self.vk_id = vk_id
        self.__save_user()

    def change_insta_id(self, insta_id):
        self.insta_id = insta_id
        self.__save_user()

    def change_money(self, money):
        self.money = money
        self.__save_user()


    def add_task(self, **kwargs):
        while True:
            task_id = randint(10000001, 99999999) # 8 digit id
            if self.fetch_task_by_id(task_id) == None:
                break
        if self.role == "Заказчик":
            self.insert_task(self.user_id, task_id,
                             kwargs['actions'],
                             kwargs['task_social'],
                             kwargs['task_name'],
                             kwargs['task_link'])

    def accept_task(self, task_id):
        task = self.fetch_task_by_id(task_id)

        if self.role != "Исполнитель":
            raise Exception("Role should be 'Исполнитель'")

        if self.user_id == task[1]:
            raise Exception("Executor id equals customer id")

        if bool(task[6]):
            raise Exception("Task done already")

        if task[2] != None:
           raise Exception("Executor already exist")

        self.update_task(task_id, executor_id=self.user_id)



    def check_task(self, task_id):
        # TODO make checker via parsers
        task = self.fetch_task_by_id(task_id)

        if task[4] == "instagram":
            pass

        elif task[4] == "vk":
            pass

        elif task[4] == "telegram":
            pass



if __name__ == '__main__':
    i = User(1, "Заказчик")
    #i.add_task("vk", "like", "dislive.me")
    #i.add_task("insta", "follow", "bash.im")
    print(i.fetch_tasks_by_customer(i.user_id))