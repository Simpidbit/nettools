import threading
import time
import ctypes

def main(msg):
	while True:
		print(msg)
		time.sleep(1)

class Thread(threading.Thread):
	def __init__(self,*args,**kwargs):
		super(Thread,self).__init__(*args,**kwargs)

	def stop(self):
		ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident),ctypes.py_object(SystemExit))

msg = "fuck"
s = Thread(target=main,args=(msg,))
s.start()
time.sleep(5)
s.stop()
print()
