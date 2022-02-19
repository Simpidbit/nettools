import os
import sys
import sqlite3
if os.system("C:"):
	pass
else:
	print("请在 Linux 系统下运行本工具！！")
	os.system("pause")
	sys.exit()
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
			1.	ghost port
			2.	ghost ip
			3.	dos attack
			4.	catch packages
			5.	exit
			<<<<<<<<<<<<							"你是个可怕的人"
			>>>>>>>>>>>>									—— 127.0.0.1
			|====================|
			|==={   }====================| So, Input something."""

functions = {
			"1":lambda:one("sudo python find_port.ghostwork a b","find_port.ghostwork","2"),
			"2":lambda:one("sudo python find_ip.ghostwork","find_ip.ghostwork","1"),
			"3":lambda:one("sudo python dos.ghostwork","dos.ghostwork","3"),
			"4":lambda:print("catch packages")
			}

def one(s,file_name,file_id):
	conn = sqlite3.connect("codes.db")
	cur = conn.cursor()
	with open(file_name,"w",encoding="utf-8") as f:
		cmd = "select main from code where id="+file_id
		for each in cur.execute(cmd):
			code = each[0]
		f.write(code)
	os.system(s)

while True:
	os.system("clear")
	print(s,end="")
	b = '\b'
	print(f"{b*45}",end="")
	
	temp = input()
	if temp == "5":
		break
	try:
		functions[temp]()
		os.system("rm -f *.ghostwork")
		os.system("sudo python index.py")
		break
	except:
		print("wrong")

os.system("clear")
