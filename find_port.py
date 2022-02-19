from scapy.all import *
from threading import Thread
import dns.resolver
import sys
import time
import os
os.system("clear")
if len(sys.argv) >= 2:
	pass
else:
	os.system("gnome-terminal --maximize -t \"端口扫描器 by GhostWorker\" -- sudo python3 find_port.py a b")
	exit()
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
print(s)
# 获取用户输入
ip = input("[  GET  ] <== 请输入目标ip地址:")
port_min_and_max = input("[  GET  ] <== 请输入端口范围(默认1-65535):")

# 如果是空串,为port_min_and_max设置默认值
if port_min_and_max == "":
	port_min_and_max = "1-65535"

port_min = int(port_min_and_max.split("-")[0])
port_max = int(port_min_and_max.split("-")[1])
port_all = port_max+1 - port_min

ports = []

def check(pkt,ports,ip,is_exit):
	if is_exit[0]:
		exit()
	for i in ip:
		if pkt.sprintf("{IP:%IP.src%}") == i:
			ports.append(int(pkt.sprintf("{IP:%IP.sport%}")))
		else:
			print(pkt.sprintf("{IP:%IP.src%}")," --- ",i)

def listen(ports,ip,is_exit):
	sniff(count=0,prn=lambda pkt:check(pkt,ports,ip,is_exit))

is_exit = [False,]
dns_ip = []
A = dns.resolver.query(ip,'A')
for i in A.response.answer:
	for j in i.items:
		dns_ip.append(str(j))

print("[  Tips  ] ==> DNS解析服务已经解析到的IP地址: " ,dns_ip)
Thread(target = listen, args = (ports, dns_ip, is_exit)).start()

stream = sys.stdout
sys.stdout = None

def printf(s):
	sys.stdout = stream.write(s)
	sys.stdout = None

c = "="
now = 0
for port in range(port_min, port_max+1):
	print("start")
	Thread(target=send, args=(IP(dst=ip) / TCP(dport=port),)).start()
	now += 1
	time.sleep(0.005)
	printf(f"\r[ Status ] ==> %d%% [{c*int(now/port_all*100)}]"% (now/port_all*100))

time.sleep(1)
printf("\n\r[   OK   ] ==> 扫描完毕，对 %d 个端口进行了扫描，发送 %d 个数据包，收到 %d 个\n" % (port_all,now,len(ports)))
is_exit[0] = True
ports.sort()
_ports = []
for each in ports:
	no = False
	for j in _ports:
		if j == each:
			no = True
			break
	if not no:
		_ports.append(each)
sys.stdout = stream
print("[   OK   ] ==> 共发现 %d 个端口，端口号为:"%len(_ports),end="")
times = 0
if len(_ports) > 4:
	print("\n\t",end="")
else:
	print("\t",end="")
for each in _ports:
	if len(_ports) <=4:
		sys.stdout.write("["+str(each)+"]"+"\t\t")
		continue
	sys.stdout.write("["+str(each)+"]"+"\t\t")
	times += 1
	if times >= 7:
		print("\n\t",end="")
		times = 0
print("\n请按回车键继续...")
input()
print("\r[ Status ] ==> 正在清理线程...")
sys.exit()
