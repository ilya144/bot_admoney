import sqlite3


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
                               insta_id=None, money=None):

        sql_str = ""

        if vk_id!=None:
            sql_str += f"vk_id={vk_id}, "

        if insta_id!=None:
            sql_str += f"insta_id={insta_id}, "

        if referal!=None:
            sql_str += f"referal={referal}, "

        if money!=None:
            sql_str += f"money={money}, "


        sql_str = sql_str.rstrip(", ")
        return sql_str

    def __update_columns_tasks(self,
                               customer_id=None, executor_id=None,
                               task_social=None, task_name=None,
                               task_link=None, status=None):

        sql_str = ""

        if customer_id != None:
            sql_str += f"customer_id={customer_id}, "

        if executor_id != None:
            sql_str += f"executor_id={executor_id}, "

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
        user_id means telegram_id
        :param cur:
        :return:
        """
        try:
            cur.execute("create table users ("
                        "user_id int unique, "
                        "vk_id int null unique, "
                        "insta_id int null unique, "
                        "referal int, "
                        "money real)")
        except:
            pass

    def __create_task_table(self, cur):

        try:
            cur.execute("create table tasks ("
                        "task_id int unique, "
                        "customer_id int, "
                        "executor_id int null, "
                        "task_social text, "
                        "task_name text, "
                        "task_link text, "
                        "status int)")
        except:
            pass



    def __init__(self, db_name):
        self.conn = None
        self.db_name = db_name
        cur = self.__connect_db()

        self.__create_user_table(cur)
        self.__create_task_table(cur)

        self.__close_db()



    ########### USER MANAGEMENT ###########
    def insert_user(self, user_id, referal, money):
        cur = self.__connect_db()
        cur.execute("insert into users values("
                    f"{user_id}, null, null, "
                    f"{referal}, {money})")
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
        :return:
        """
        set_sql = self.__update_columns_users(
            vk_id=kwargs.get("vk_id"),
            insta_id=kwargs.get("insta_id"),
            referal=kwargs.get("referal"),
            oney=kwargs.get("money")
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
    def insert_task(self, customer_id, task_id,
                   task_social, task_name, task_link):

        cur = self.__connect_db()
        cur.execute("insert into tasks values ("
                    f"{task_id}, {customer_id}, null,"
                    f" '{task_social}', "
                    f" '{task_name}', "
                    f" '{task_link}', "
                    "0)")
        self.__commit_db()
        self.__close_db()

    def update_task(self, task_id, **kwargs):
        """

        :param task_id: unique id of task
        :param kwargs:
                : customer_id: who pay and create task
                : executor_id: who accept and work
                : task_social: vk, insta or telegram
                : task_name: like, follow, etc
                : task_link: url to object of task
                : status: 0 - in progress; 1 - complete
        :return:
        """
        set_sql = self.__update_columns_tasks(
            customer_id=kwargs.get("customer_id"),
            executor_id=kwargs.get("executor_id"),
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
