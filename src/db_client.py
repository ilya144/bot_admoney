import sqlite3
import time


class Database:
    ########### UTILITY ###########
    def __connect_db(self):
        self.conn = sqlite3.connect(self.db_name)
        cur = self.conn.cursor()
        return cur

    def __close_db(self):
        self.conn.close()

    def __commit_db(self):
        self.conn.commit()


    def __update_columns_users(self,
                               referal=None, vk_id=None,
                               insta_id=None, money=None,
                               subscribe=None):

        sql_str = ""

        if vk_id!=None:
            sql_str += f"vk_id='{vk_id}', "

        if insta_id!=None:
            sql_str += f"insta_id='{insta_id}', "

        if referal!=None:
            sql_str += f"referal={referal}, "

        if money!=None:
            sql_str += f"money={money}, "

        if subscribe!=None:
            sql_str += f"subscribe={subscribe}, "


        sql_str = sql_str.rstrip(", ")
        return sql_str

    def __update_columns_tasks(self,
                               customer_id=None, actions=None,
                               task_social=None, task_name=None,
                               task_link=None, status=None):

        sql_str = ""

        if customer_id != None:
            sql_str += f"customer_id={customer_id}, "

        if actions != None:
            sql_str += f"actions={actions}, "

        if task_social != None:
            sql_str += f"task_social='{task_social}', "

        if task_name != None:
            sql_str += f"task_name='{task_name}', "

        if task_link != None:
            sql_str += f"task_link='{task_link}', "

        if status != None:
            sql_str += f"status={status}, "


        sql_str = sql_str.rstrip(", ")
        return sql_str

    def __create_user_table(self, cur):
        """
        user_id means telegram_id,
        insta and vk id actually means usernames
        (sorry for misunderstanding)

        subscribe column like a chmod linux
        {4: Инстаграм, 2: ВК, 1: Телеграм}
        7 all, 0 no one

        """
        try:
            cur.execute("create table users ("
                        "user_id int unique, "
                        "vk_id text null unique, "
                        "insta_id text null unique, "
                        "referal int, "
                        "money real, "
                        "subscribe int, "
                        "primary key (user_id))")
        except Exception as e:
            if (str(e) == "table users already exists"):
                pass
            else:
                print(str(e))

    def __create_task_table(self, cur):

        try:
            cur.execute("create table tasks ("
                        "task_id int unique, "
                        "customer_id int, "
                        "actions int, "
                        "task_social text, "
                        "task_name text, "
                        "task_link text, "
                        "status int, "
                        "time int, "
                        "primary key (task_id))")
                        #"ON DELETE CASCADE)") # ? добавил, гляну шо будет
        except Exception as e:
            if (str(e) == "table tasks already exists"):
                pass
            else:
                print(str(e))

    def __create_executors_table(self, cur):

        try:
            cur.execute("create table executors ("
                        "user_id int references users(user_id)"
                        "on delete cascade, "
                        "task_id int references tasks(task_id)"
                        "on delete cascade,"
                        "status int"
                        ")")
        except Exception as e:
            if (str(e) == "table executors already exists"):
                pass
            else:
                print(str(e))



    def __init__(self, db_name):
        self.conn = None
        self.db_name = db_name
        cur = self.__connect_db()

        self.__create_user_table(cur)
        self.__create_task_table(cur)
        self.__create_executors_table(cur)

        self.__close_db()



    ########### USER MANAGEMENT ###########
    def insert_user(self, user_id, referal, money, subscribe=0):
        cur = self.__connect_db()
        cur.execute("insert into users values("
                    f"{user_id}, null, null, "
                    f"{referal}, {money}, {subscribe})")
        self.__commit_db()
        self.__close_db()
        return True

    def update_user(self, user_id, **kwargs):
        """

        :param user_id: id in telegram
        :param kwargs:
                : vk_id: actually VK id, not username
                : insta_id: same, fetched by username
                : referal: amount of invited users
                : money: user money in rubles
                : subscribe: get new tasks
        :return:
        """
        set_sql = self.__update_columns_users(
            vk_id=kwargs.get("vk_id"),
            insta_id=kwargs.get("insta_id"),
            referal=kwargs.get("referal"),
            money=kwargs.get("money"),
            subscribe=kwargs.get("subscribe")
        )
        cur = self.__connect_db()
        cur.execute(f"update users set {set_sql} "
                    f"where user_id={user_id}")
        self.__commit_db()
        self.__close_db()

    def delele_user(self, user_id):
        cur = self.__connect_db()
        cur.execute("delete from users "
                    f"where user_id = {user_id}")
        self.__commit_db()
        self.__close_db()

    def fetch_user_by_id(self, user_id):
        cur = self.__connect_db()
        user = cur.execute("select * from users "
                           f"where user_id={user_id}"
                           ).fetchone()
        self.__commit_db()
        self.__close_db()
        return user



    ########### TASK MANAGEMENT ###########
    def insert_task(self, customer_id, task_id, actions,
                   task_social, task_name, task_link):

        unix_time = int(time.time())
        cur = self.__connect_db()
        cur.execute("insert into tasks values ("
                    f"{task_id}, {customer_id}, "
                    f"{actions}, "
                    f" '{task_social}', "
                    f" '{task_name}', "
                    f" '{task_link}', "
                    f"0,{unix_time})"
                    )
        self.__commit_db()
        self.__close_db()

    def update_task(self, task_id, **kwargs):
        """

        :param task_id: unique id of task
        :param kwargs:
                : customer_id: who pay and create task
                : actions: count of max executors
                : task_social: vk, insta or telegram
                : task_name: like, follow, etc
                : task_link: url to object of task
                : status: 0 - in progress; 1 - complete
        :return:
        """
        set_sql = self.__update_columns_tasks(
            customer_id=kwargs.get("customer_id"),
            actions=kwargs.get("actions"),
            task_social=kwargs.get("task_social"),
            task_name=kwargs.get("task_name"),
            task_link=kwargs.get("task_link"),
            status = kwargs.get("status")
        )
        cur = self.__connect_db()
        cur.execute(f"update tasks set {set_sql} "
                    f"where task_id={task_id}")
        self.__commit_db()
        self.__close_db()

    def delele_task(self, task_id):
        cur = self.__connect_db()
        cur.execute("delete from tasks "
                    f"where task_id = {task_id}")
        self.__commit_db()
        self.__close_db()

    def fetch_task_by_id(self, task_id):
        cur = self.__connect_db()
        task = cur.execute("select * from tasks "
                           f"where task_id = {task_id}"
                           ).fetchone()
        self.__commit_db()
        self.__close_db()
        return task

    def fetch_tasks_by_customer(self, user_id):
        cur = self.__connect_db()
        tasks = cur.execute("select * from tasks "
                           f"where customer_id = {user_id} "
                            "order by time desc"
                           ).fetchall()
        self.__commit_db()
        self.__close_db()
        return tasks

    def fetch_tasks_by_attr(self, task_social, task_name):
        cur = self.__connect_db()
        tasks = cur.execute("select * from tasks "
                            f"where task_social = '{task_social}' "
                            f"and task_name = '{task_name}' "
                            "order by time desc"
                            ).fetchall()
        self.__commit_db()
        self.__close_db()
        return tasks



    ########### EXECUTORS MANAGEMENT ###########
    def insert_executor(self, user_id, task_id, status):
        cur = self.__connect_db()
        cur.execute("insert into executors values ("
                    f"{user_id}, {task_id}, {status})"
                    )
        self.__commit_db()
        self.__close_db()

    def fetch_tasks_by_executor(self, user_id):
        cur = self.__connect_db()
        query = "select task_id, customer_id, " \
                "actions, task_social, task_name, " \
                "task_link, status, time from" \
                "users inner join executors" \
                "on tasks.user_id = executors.task_id"

        tasks = cur.execute(query).fetchall()
        self.__commit_db()
        self.__close_db()
        return tasks

    def fetch_executors_by_tasks(self, task_id):
        cur = self.__connect_db()
        query = "select user_id, vk_id, insta_id," \
                "referal, money, subscribe" \
                "from tasks inner join executors" \
                "on users.task_id = executors.task_id"

        users = cur.execute(query).fetchall()
        self.__commit_db()
        self.__close_db()
        return users
