from scapy.all import *
import threading
import time
import socket
import ctypes
import os
import sys
import config

os.system("clear")
print("Hello! 开心点!")

already_recv = [False,]
def test(port):
	now = time.time()
	sr1(IP(dst=config.TESTIP) / TCP(dport=port))
	end = time.time()
	if end - now <= 0.5:
		print("您的服务器感觉不错")
	elif end - now <= 1:
		print("您的服务器正在努力工作...")
	elif end - now <= 2:
		print("您的服务器有点累了")
	elif end - now <= 3:
		print("您的服务器感觉很累")
	else:
		print("您的服务器正处于危险之中！")
	already_recv[0] = True

class Thread(threading.Thread):
	def __init__(self,*args,**kwargs):
		super(Thread,self).__init__(*args,**kwargs)
	
	def stop(self):
		print("您的服务器无回应,小心!")
		ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident),ctypes.py_object(SystemExit))
port = config.TESTPORT
print("正在检测您的服务器 %s 端口状态..."%str(port))
test_th = Thread(target = test,args = (port,))
test_th.start()
time.sleep(1)
if not already_recv[0]:
	time.sleep(3)
	test_th.stop()
input("请按回车键继续...")


def get_arg_info(arg):
	arg_main = arg.split(":")[0]
	try:
		arg_value = arg.split(":")[1]
	except:
		arg_value = "None of arguments"
	return (arg_main,arg_value)

class cmd:
	def __init__(self,s,version_msg):
		self.main = s.split(" ")[0]
		if len(s.split(" ")) == 1:
			return
		self._arguments = s.split(" ")[1:]
		self.arguments = {}
		for each in self._arguments:
			self.arguments[get_arg_info(each)[0]]=get_arg_info(each)[1]
		self.version_msg = version_msg
		print(self.arguments)
		input()

		def v_main(self):
			if self.main == "version":
				print("Ghost protecter by GhostWorker (QQ:2766277617)\nversion:1.0")

		def ip_main(self):
			if self.main == "ip":
				s = socket.socket()
				s.connect((config.SHELLIP,config.SHELLPORT))
				try:
					s.send(("ipadd"+" "+self.arguments["add"]).encode())
				except:
					try:
						s.send(("ipremove"+" "+self.arguments["remove"]).encode())
					except:
						s.send("seeip".encode())
						while True:
							time.sleep(0.1)
							res = s.recv(1024).decode()
							if not res == "end":
								print("封禁IP:",res.split(" ")[0],"\t\t封禁时间:",res.split(" ")[-1])
							else:
								print("完毕")
								break
				s.close()
				input("请按回车键继续...")

		def help_main(self):
			if self.main == "help":
				with open("help","r") as f:
					print(f.read())

		def exit_main(self):
			if self.main == "exit":
				raise SystemExit

		def run(self):
			v_main(self)
			ip_main(self)
			help_main(self)
			exit_main(self)
		run(self)

while True:
	os.system("clear")
	cmd(input("[ INPUT ] So,make a decision:"),"a")
