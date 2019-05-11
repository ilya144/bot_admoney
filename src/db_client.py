import sqlite3


class Database:
    def __connect_db(self):
        self.conn = sqlite3.connect(self.db_name)
        cur = self.conn.cursor()
        return cur

    def __close_db(self):
        self.conn.close()

    def __commit_db(self):
        self.conn.commit()

    def __update_columns(self, _referal=None, _vk_id=None,
                  _insta_id=None, _money=None):

        sql_str = ""
        if _vk_id!=None:
            sql_str += f"vk_id={_vk_id}"
        if _insta_id!=None:
            sql_str += f"instagram_id={_insta_id}"
        if _referal!=None:
            sql_str += f"referal={_referal}"
        if _money!=None:
            sql_str += f"money={_money}"

        return sql_str


    def __init__(self, db_name):
        self.conn = None
        self.db_name = db_name
        cur = self.__connect_db()
        # user_id means telegram_id
        try:
            cur.execute("create table users (user_id int unique, "
                        "vk_id int null unique, "
                        "insta_id int null unique, "
                        "referal int, money real)")
        except:
            pass
        self.__close_db()

    def insert_user(self, _id, _referal, _money):
        cur = self.__connect_db()
        cur.execute(f"insert into users values("
                    f"{_id}, null, null, {_referal}, {_money})")
        self.__commit_db()
        self.__close_db()
        return True

    def update_user(self, _id, **kwargs):
        """

        :param _id:
        :param kwargs:
                : _vk_id: actually VK id, not username
                : _insta_id: same, fetched by username
                : _referal: amount of invited users
                : _money: user money in rubles
        :return:
        """
        set_sql = self.__update_columns(
            _referal=kwargs.get("_referal"),
            _vk_id=kwargs.get("_vk_id"),
            _insta_id=kwargs.get("_insta_id"),
            _money=kwargs.get("_money")
        )
        cur = self.__connect_db()
        cur.execute(f"update users set {set_sql}"
                    f" where user_ud='{_id}'")

    def fetch_user_by_id(self, _id):
        cur = self.__connect_db()
        user = cur.execute(f"select * from users "
                           f"where user_id='{_id}'").fetchone()
        self.__commit_db()
        self.__close_db()
        return user

