import sqlite3 as sq


conn = sq.connect("Word_dataset.db")
cursor = conn.cursor()
cursor.execute("select * from word_dataset where word_index = ?",(130,))
data = (list((cursor.fetchall())[0]))[1]
print(data.split(','))


