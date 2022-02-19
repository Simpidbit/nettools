from scapy.all import *
from threading import Thread
import sqlite3
import config
import socket
import time
import os

connections = {}

class connection:
	def __init__(self):
		self.times = 1
		self.connect_time = None

def catch_ip():
	def main(pkt):
		ip = pkt.sprintf("{IP:%IP.src%}")
		try:
			connections[ip]
		except:
			connections[ip] = connection()
			connections[ip].connect_time = int(time.time())
		connections[ip].times += 1
	sniff(count=0, prn=main)
Thread(target=catch_ip).start()

con_db = sqlite3.connect("kill_ip.db",check_same_thread = False)
cur_db = con_db.cursor()

def shell_cmd():
	s = socket.socket()
	s.bind((config.BINDIP,config.SHELLPORT))
	s.listen(2)
	while True:
		conn,addr = s.accept()
		shell_recv = conn.recv(1024).decode()

		ip = shell_recv.split(" ")[-1]
		print("ip is",ip)
		if "ipadd" in shell_recv:
			for each in cur_db.execute("select ip from ip_connections"):
				if each[2] == ip:
					temp = True
			if temp:
				temp = False
				continue
			os.system("sudo iptables -I INPUT -s %s -j DROP" % ip)
			insert_cmd = "insert into ip_connections(id,ip,time) values(?,?,?)"
			data = ([i[0] for i in cur_db.execute("select id from ip_connections")][0],ip,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
			cur_db.execute(insert_cmd,data)
			con_db.commit()
		elif "ipremove" in shell_recv:
			os.system("sudo iptables -D INPUT -s %s -j DROP" % ip)
			cur_db.execute("delete from ip_connections where ip=\"%s\"" % ip)
			con_db.commit()
		elif "seeip" in shell_recv:
			for each in cur_db.execute("select * from ip_connections"):
				conn.sendall((each[1]+" "+each[2]).encode())
				time.sleep(0.1)
			conn.sendall("end".encode())
		conn.close()
Thread(target=shell_cmd).start()
try:
	cur_db.execute("create table ip_connections(id int,ip text,time text)")
	cur_db.execute("insert into ip_connections(id,ip,time) values(?,?,?)",(1,"hello, I'm Ghostworker","9012/13/32"))
	con_db.commit()
except:
	pass

will_pop = []
while True:
	for each in will_pop:
		connections.pop(each)
	will_pop = []
	connections_temp = connections.copy()
	for each in connections_temp:
		if connections_temp[each].times >= config.KILLTIMES:
			if not each == [i for i in config.CANNOTKILL][0]:
				os.system("sudo iptables -i INPUT -s %s -j DROP" % each)
				insert_cmd = "insert into ip_connections(id,ip,time) values(?,?,?)"
				data = ([i[0] for i in cur_db.execute("select id from ip_connections")][0],each,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
				cur_db.execute(insert_cmd,data)
				con_db.commit()

		if connections_temp[each].connect_time <= int(time.time()-config.KILLSECOND):
			will_pop.append(each)
