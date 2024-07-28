import pvaccess
import time
from flask import Flask

app = Flask(__name__)

SERVER_ADDR = 'localhost'

dbSample = [
    {'pvname':'scwook:ai1', 'state':'alarm', ''}
    ]

c = pvaccess.Channel('scwook:ai1')
count = 0

def echo(x):
    global count
    count += 1
    print('count', count)

c.subscribe('echo', echo)
c.startMonitor()

@app.route('/', methods=['GET'])
def test():
    return "OK"

if __name__ == "__main__":
    app.run(host=SERVER_ADDR, port="8000")