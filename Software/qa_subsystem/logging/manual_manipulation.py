import sqlite3
from datetime import datetime

con = sqlite3.connect('query_logs.db')
cur = con.cursor()

# def insert():
#     print("INSERTING")
# cur.execute('''INSERT INTO query_logs VALUES(?,?)''', ('Sample Query', datetime.now()))
# con.commit()


# def select():
#     print("SELECTING")
results = cur.execute('''SELECT * FROM query_logs''')
print(results.fetchall())

# if __name__ == "__main__":
#     a = input("Insert - 1, Select - 2")
#     print(a)
#     if a == 1:
#         insert()
#     if a == 2:
#         select()