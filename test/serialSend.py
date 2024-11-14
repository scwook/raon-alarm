import time
import serial
import multiprocessing
import queue

import os

PORT = '/dev/tty.usbserial-FT96QAFW'

ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)

def sendQueue(queue):
    count = 0
    while True:
        count += 1
        data = f'id: {os.getpid()}, count: {count}' 
        # print(f'id: {os.getpid()}, count: {count}')
        queue.put(data)
        time.sleep(1)

def readQueue(q):
    while True:
        try:
            data = q.get(block=False)
            print(data)
            ser.write(data.encode('utf-8') + b'\r\n')

        except queue.Empty:
            print('empty')
            pass

        time.sleep(0.1)    

if __name__ == "__main__":
    queue = multiprocessing.Queue()

    process1 = multiprocessing.Process(target=sendQueue, args={queue})
    process2 = multiprocessing.Process(target=sendQueue, args={queue})
    process3 = multiprocessing.Process(target=sendQueue, args={queue})

    queueProcess = multiprocessing.Process(target=readQueue, args={queue})
    process1.start()
    process2.start()
    process3.start()
    queueProcess.start()

    process1.join()
    process2.join()
    process3.join()
    queueProcess.join()