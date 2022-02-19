import sqlite3
import os

# os.system("rm -f codes.db")
s = sqlite3.connect("codes.db")
cur = s.cursor()

cmd = "create table code(id int,name text,main text)"
# cur.execute(cmd)

cmd = "insert into code(id,name,main) values(?,?,?)"

with open("find_ip.py","r") as f:
	main_code = f.read()
data = (1,"find_ip",main_code)
# cur.execute(cmd,data)

with open("find_port.py","r") as f:
	main_code = f.read()
data = (2,"find_port",main_code)
# cur.execute(cmd,data)

with open("dos.py","r") as f:
	main_code = f.read()
data = (3,"dos",main_code)
# cur.execute(cmd,data)
# s.commit()

for each in cur.execute("select main from code where id=1"):
	print(each[0])
