import threading
import time

th = None

def test():
    print('aaa')
    global th
    th = threading.Timer(1, test)
    th.start()



th = threading.Timer(1, test)
th.start()

count = 0
while True:
    time.sleep(1)
    count += 1
    print('thread', th)
    print(th.is_alive())
    if count == 10:
        th.cancel()
        print(count, th)
        print(th.is_alive())