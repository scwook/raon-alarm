import serial
import time
import multiprocessing
import queue

PORT = '/dev/tty.usbserial-FT96QAFW'
try:
    ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)
except serial.SerialException as e:
    print(e)


def userInput(q):
    while True:

        user = input('Send data:')
        q.put(user)

        time.sleep(1)

def waitConnection():
    while not ser.is_open:
        try:
            ser.open()
        except serial.SerialException:
            pass

        print('wait conneciotn')
        time.sleep(1)

    print(ser.is_open)

def sendMessage(q):
    while True:
        try:
            data = q.get(block=False)
            if ser.is_open:
                ser.write(data.encode('utf-8'))
                print('Send data: ', data)

        except queue.Empty:
            # print('queue empty')
            pass

        except serial.SerialException as e:
            ser.close()
            print(ser.is_open, e)
            print('waite connection')
            waitConnection()

        time.sleep(1)

if __name__ == "__main__":
    q = multiprocessing.Queue()

    # process1 = multiprocessing.Process(target=userInput, args={q})
    process = multiprocessing.Process(target=sendMessage, args={q})
    process.start()

    while True:
        user = input('Input data: ')
        q.put(user)
        time.sleep(1)