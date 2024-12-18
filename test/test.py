import threading
import asyncio
import time

def valueconversion(valueType, value):
    if valueType == "DOUBLE":
        return float(value)
    elif valueType == "INT":
        return int(value)
    else:
        return value
    
def alarmDelay():
    print('stop')
    
val = 12.5
a = valueconversion("INT", val)
print(type(a))
print(a)

timer = threading.Timer(5, alarmDelay)
timer.start()

time.sleep(5)
print('time sleep')

