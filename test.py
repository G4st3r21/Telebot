from datetime import datetime as dt

time = str(dt.now())[:16]

print(time)

with open('db/AllTables.db', 'r') as file:
    print(file)