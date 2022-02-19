import sqlite3

conn = sqlite3.connect("pkt.db")
cur = conn.cursor()

for i in cur.execute("select * from packages"):
	print(i)
	input()
