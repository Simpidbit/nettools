import socket
import sys
from threading import Thread
import time
import os

socket.setdefaulttimeout(2)

s = r"""**********************************************************************************************************************************************
             ('-. .-.               .-')    .-') _     (`\ .-') /`             _  .-')  .-. .-')     ('-.  _  .-')   
            ( OO )  /              ( OO ). (  OO) )     `.( OO ),'            ( \( -O ) \  ( OO )  _(  OO)( \( -O )  
  ,----.    ,--. ,--. .-'),-----. (_)---\_)/     '._ ,--./  .--.   .-'),-----. ,------. ,--. ,--. (,------.,------.  
 '  .-./-') |  | |  |( OO'  .-.  '/    _ | |'--...__)|      |  |  ( OO'  .-.  '|   /`. '|  .'   /  |  .---'|   /`. ' 
 |  |_( O- )|   .|  |/   |  | |  |\  :` `. '--.  .--'|  |   |  |, /   |  | |  ||  /  | ||      /,  |  |    |  /  | | 
 |  | .--, \|       |\_) |  |\|  | '..`''.)   |  |   |  |.'.|  |_)\_) |  |\|  ||  |_.' ||     ' _)(|  '--. |  |_.' | 
(|  | '. (_/|  .-.  |  \ |  | |  |.-._)   \   |  |   |         |    \ |  | |  ||  .  '.'|  .   \   |  .--' |  .  '.' 
 |  '--'  | |  | |  |   `'  '-'  '\       /   |  |   |   ,'.   |     `'  '-'  '|  |\  \ |  |\   \  |  `---.|  |\  \  
  `------'  `--' `--'     `-----'  `-----'    `--'   '--'   '--'       `-----' `--' '--'`--' '--'  `------'`--' '--' 
**********************************************************************************************************************************************
"""

class iplist:
	def __init__(self, ip):
		self.ip = ip
		self.list = [int(i) for i in ip.split(".")]

	def get_ip(self):
		return str(self.list[0]) + "." + str(self.list[1]) + "." + str(self.list[2]) + "." + str(self.list[3])

os.system("clear")
print(s)
begin_address = input("[   GET   ] <== 请输入开始IP地址: ")
end_address = input("[   GET   ] <== 请输入结束IP地址: ")
ip_pool = []

# 开始计算地址
# 192.168.2.20 - 192.168.5.250
begin_address_list = iplist(begin_address)
end_address_list = iplist(end_address)

different = [0,0,0,0]
dif_index = []
for i in range(4):
	if not begin_address_list.list[i] == end_address_list.list[i]:
		different[i] = end_address_list.list[i] - begin_address_list.list[i]
		dif_index.append(i)

# dif = [2,3]
# dif = [1,2,3]
temp = {}
for i in dif_index:
	temp[i] = []
	for j in range(different[i]+1):
		temp[i].append(begin_address_list.list[i] + j)

# 1位
if len(dif_index) == 1:
	for each in temp:
		for i in temp[each]:
			begin_address_list.list[each] = i
			ip_pool.append(begin_address_list.get_ip())

# 2位
elif len(dif_index) == 2:
	for each in temp:
		for i in temp[each]:
			for j in temp:
				if not j == each:
					for k in temp[j]:
						begin_address_list.list[each] = i
						begin_address_list.list[j] = k
						ip_pool.append(begin_address_list.get_ip())

# 3位
elif len(dif_index) == 3:
	for each in temp:
		for i in temp[each]:
			for j in temp:
				if not j == each:
					for k in temp[j]:
						for a in temp:
							if (not a == each) and (not a == j):
								for b in temp[a]:
									begin_address_list.list[each] = i
									begin_address_list.list[j] = k
									begin_address_list.list[a] = b
									ip_pool.append(begin_address_list.get_ip())


print("------------------------------------------------------------------")

# 将重复的剔除
temp = [0,]
for each in ip_pool:
	had = False
	for t in temp:
		if t == each:
			had = True
			break
	if not had:
		temp.append(each)
temp.pop(0)
ip_pool = temp
temp = None

# 获取端口
temp = input("[   GET   ] <== 请输入探测的端口(多个端口用逗号隔开):")
temp = temp.split(",")
temp = list(temp)
for i in range(len(temp)):
	temp[i] = int(temp[i])
ports = temp

in_loop = [True,]
trueip = []
packages = []

def see(s,tu):
	try:
		s.connect(tu)
		print("[ status ] !! 收到来自",tu[0],"的",tu[1],"端口数据包回复")
		if not tu[0] in trueip:
			trueip.append(tu[0])
		if not (tu[0],str(tu[1])) in packages:
			packages.append((tu[0],str(tu[1])))
	except:
		pass

jindu = 0
_all = len(ip_pool)*len(ports)
now_jindu = 0
for port in temp:
	for ip in ip_pool:
		s = socket.socket()
		Thread(target=see, args=(s,(ip,port))).start()
		time.sleep(0.005)
		jindu += 1
		if now_jindu == 0:
			if int(jindu/_all*100) == 25:
				print("[ status ] ==> 已完成 25%% ")
				now_jindu = 25
		elif now_jindu == 25:
			if int(jindu/_all*100) == 50:
				print("[ status ] ==> 已完成 50%%")
				now_jindu = 50
		elif now_jindu == 50:
			if int(jindu/_all*100) == 75:
				print("[ status ] ==> 已完成 75%%")
				now_jindu = 75
		elif now_jindu == 75:
			if int(jindu/_all*100) == 100:
				print("[ status ] ==> 已完成扫描")
				now_jindu = 100

time.sleep(3)
def sort_ip():
	nothing = True
	while nothing:
		nothing = False
		for each in range(1,len(trueip)):
			for i in range(len(trueip[each-1].split("."))):
				if int(trueip[each].split(".")[3]) < int(trueip[each-1].split(".")[3]):
					temp = trueip[each-1]
					trueip[each-1] = trueip[each]
					trueip[each] = temp
					nothing = True
	nothing = True
	while nothing:
		nothing = False
		for each in range(1,len(trueip)):
			for i in range(len(trueip[each-1].split("."))):
				if int(trueip[each].split(".")[2]) < int(trueip[each-1].split(".")[2]):
					temp = trueip[each-1]
					trueip[each-1] = trueip[each]
					trueip[each] = temp
					nothing = True
	nothing = True
	while nothing:
		nothing = False
		for each in range(1,len(trueip)):
			for i in range(len(trueip[each-1].split("."))):
				if int(trueip[each].split(".")[1]) < int(trueip[each-1].split(".")[1]):
					temp = trueip[each-1]
					trueip[each-1] = trueip[each]
					trueip[each] = temp
					nothing = True

in_loop[0] = False

print("[ status ] ==> 正在整理数据...")
sort_ip()
print("[ status ] ==> 数据整理完毕！")

time.sleep(2)
print("[ status ] ==> 本次共扫描 %d 个 ip 地址，获得了 %d 个回包，共探测到 %d 个存在的 IP 地址:" % (_all,len(packages),len(trueip)))
for i in trueip:
	for j in packages:
		if i in j:
			print("ip地址:",i,"\t\t端口:",j[1])
print("============================================================")
print("IP 地址: ")
times = 0
for i in trueip:
	print("\t",i,end="")
	times += 1
	if times >= 5:
		print()
		times = 0
input()
sys.exit()
