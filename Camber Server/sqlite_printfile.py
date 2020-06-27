



import sqlite3



conn=sqlite3.connect("log.db")
cur=conn.cursor()

cur.execute("SELECT * FROM logbook")

print(cur.fetchall())