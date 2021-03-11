import sqlite3

con = sqlite3.connect('db/AllTables.db')
cur = con.cursor()


class Tasks():
    def __init__(self):
        self.con = sqlite3.connect('db/AllTables.db')
        self.cur = con.cursor()
        self.table = 'Tasks'

    def add_to_db(self, params):
        name, done, datetime = params
        cur.execute(f'INSERT INTO {self.table} VALUES ({name}, {done}, {datetime})')
        con.commit()

        print('Добавлены данные в таблицу')
    
    def del_from_db(self, name):
        cur.execute(f'DELETE FROM {self.table} WHERE Taskname = "{name}"')
        con.commit()

        print('Удалены данные из таблицы')
    
    def change_value_done(name, done):
        cur.execute(f'SET VALUE "Done" {done} WHERE Taskname = "{name}"')

