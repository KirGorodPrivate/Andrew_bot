import sqlite3
from datetime import datetime, date, time
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

try:
    cursor.execute("""CREATE TABLE test
                        (Number int, Name text)""")
except:
    print("DB already exist!")


Name = input()

cursor.execute("INSERT INTO test(Number) VALUES(?)", (Name,))

a = []

for row in cursor.execute('SELECT Number from test'):
    a.append(row)
    print(row)