from scapy.all import *
import sqlite3

conn = sqlite3.connect("pkt.db")
cur = conn.cursor()

def main(pkt):
	cmd = "insert into packages(id,src,sport,dst,dport,length,message) values(?,?,?,?,?,?,?)"
	_id = [i[0] for i in cur.execute("select id from packages")][-1] + 1
	src = pkt.sprintf("{IP:%IP.src%}")
	try:
		sport = int(pkt.sprintf("{IP:%IP.sport%}"))
	except:
		sport = 0
	dst = pkt.sprintf("{IP:%IP.dst%}")
	try:
		dport = int(pkt.sprintf("{IP:%IP.dport%}"))
	except:
		dport = 0
	length = len(str(pkt.sprintf("{Raw:%Raw.load%}")))
	message = pkt.sprintf("{Raw:%Raw.load%}")
	cur.execute(cmd,(_id,src,sport,dst,dport,length,message))
	conn.commit()

sniff(count = 0, prn = main)
