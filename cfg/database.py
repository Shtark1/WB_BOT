import sqlite3
import time

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, usernme, nickname):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `nickname`, signup) VALUES (?, ?, ?)", (user_id, usernme, nickname,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id,))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))

    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `time_sub` = ? WHERE `user_id` = ?", (time_sub, user_id,))

    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub

    def get_sub_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            if time_sub > int(time.time()):
                return True
            else:
                return False


    def add_info_tovar(self, art, price, id_chat):
        with self.connection:
            return self.cursor.execute(f"""INSERT INTO users_products
                                      (art, price, id_chat)
                                      VALUES
                                      ({art}, {price}, {id_chat});""")

    def get_add_tovar(self, id_chat):
        with self.connection:
            result = self.cursor.execute("SELECT `art`, `price` FROM `users_products` WHERE `id_chat` = ?", (id_chat,)).fetchall()
            return result

    def delete_tovar(self, art, price, id_chat):
        with self.connection:
            result = self.cursor.execute("DELETE FROM `users_products` WHERE `art` = ? and `price` = ? and `id_chat` = ?", (art, price, id_chat)).fetchall()
            return result

    def delete_all_tovar(self, id_chat):
        with self.connection:
            result = self.cursor.execute("DELETE FROM `users_products` WHERE `id_chat` = ?", (id_chat,)).fetchall()
            return result