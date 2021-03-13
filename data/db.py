import sqlite3


class Tasks():
    def __init__(self):
        self.con = sqlite3.connect('db/AllTables.db')
        self.cur = self.con.cursor()
        self.table = 'Tasks'

    def add_to_db(self, params):
        name, done, datetime = params
        self.cur.execute(
            f'INSERT INTO {self.table}(TaskName, Done, Date) VALUES ({name}, {done}, {datetime})')
        self.con.commit()

        print('Добавлены данные в таблицу')

    def del_from_db(self, name):
        self.cur.execute(f'DELETE FROM {self.table} WHERE Taskname = "{name}"')
        self.con.commit()

        print('Удалены данные из таблицы')

    def change_value_done(self, name, done):
        self.cur.execute(
            f'UPDATE {self.table} SET Done = "{done}" WHERE Taskname LIKE "{name}"')
        self.con.commit()

        print('Изменены данные в таблице')


Tasktest = Tasks()
Tasktest.add_to_db(('aye', 0, '05.08.13 15:42:23'))
