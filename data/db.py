import sqlite3

class ReminderTable():
    def __init__(self):
        self.con = sqlite3.connect('db/AllTables.db')
        self.cur = self.con.cursor()
        self.table = 'Reminder'

    def add_to_db(self, params):
        text, datetime, user_id = params
        self.cur.execute(
            f'INSERT INTO {self.table}(Text, Date, UserID) VALUES ("{text}", "{datetime}", "{user_id}")')
        self.con.commit()

        print('Добавлены данные в таблицу')

    def del_from_db(self, text):
        self.cur.execute(f'DELETE FROM {self.table} WHERE Text = "{text}"')
        self.con.commit()

        print('Удалены данные из таблицы')
    
    def check_avaibility(self, time):
        people = self.cur.execute(
            f'SELECT * FROM {self.table} WHERE Date = {time}').fetchall()
        
        return people


class UserTable():
    def __init__(self):
        self.con = sqlite3.connect('db/AllTables.db')
        self.cur = self.con.cursor()
        self.table = 'Users'

    def add_to_db(self, params):
        UserName, UserID = params
        try:
            self.cur.execute(
                f'INSERT INTO {self.table}(UserName, UserID, WantNews) VALUES ("{UserName}", {UserID}, 0)')
            self.con.commit()
            logging.info(f'Добавлен новый пользователь: {UserName}')
            print('Новый пользователь. Добавлены данные в таблицу')
        except Exception:
            print(f'О, {UserName} поздоровался со мной!')

    def del_from_db(self, UserID):
        self.cur.execute(f'DELETE FROM {self.table} WHERE UserID = "{UserID}"')
        self.con.commit()

        print('Удалены данные из таблицы')

    def want_to_see_news(self, UserID, WantNews):
        self.cur.execute(
            f'UPDATE {self.table} SET WantNews = "{WantNews}" WHERE Taskname LIKE "{UserID}"')
        self.con.commit()

        print('Изменены данные в таблице')

    def check_Want_News(self):
        people = self.cur.execute(
            f'SELECT * FROM {self.table} WHERE WantNews = 1').fetchall()
        return people

    def check_info_by_id(self, UserID):
        return self.cur.execute(
            f'SELECT * FROM {self.table} WHERE UserID = {UserID}').fetchall()


# Tasktest = TaskTable()
# Tasktest.add_to_db(('aye', 0, '05.08.13 15:42:23', '503655279'))
# Userstest = UserTable()
# Userstest.add_to_db(('pukich', '503655279', '0'))


UsersTable = UserTable()

people = UsersTable.cur.execute("SELECT UserID FROM Users").fetchall()

for num in people:
    print(*num)