import time
from pvaccess import *

def echo(data):
    print(data)

c = Channel('COMA-CTRL:ALARM-MESS:AI1', CA)

c.subscribe('COMA-CTRL:ALARM-MESS:AI1', echo)
c.startMonitor('field(value)')

while True:
    time.sleep(0.1)