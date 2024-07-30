from pvaccess import *
import time
# from flask import Flask

# app = Flask(__name__)

SERVER_ADDR = 'localhost'

dbSample = [
    {'pvname':'scwook:ai1', 'value':5.0, 'condition':0, 'state':'normal', 'active':True, 'timestamp': '0'},
    {'pvname':'scwook:ai2', 'value':5.0, 'condition':0, 'state':'normal', 'active':False, 'timestamp': '0'}
    ]

class ChannelMonitor:
    def __init__(self, info):
        self.info = info
        self.channel = Channel(info['pvname'], ProviderType.CA)

    def monitor(self, data):
        currentValue = dict(data)
        alarmValue = self.info['value']
        alarmState = self.info['state']
        alarmActive = self.info['active']

        if currentValue['value'] > alarmValue:
            if alarmActive and alarmState == 'normal':
                print(self.info['pvname'], 'alarm')
                self.info['state'] = 'alarm'
                self.info['timestamp'] = int(time.time())
            else:
                print(self.info['pvname'], 'alarm deactive')


# c = pvaccess.Channel('scwook:ai1')
# def echo(x):
    # print('count', count)

channelList = list()
monitoringList = list()

channelList.append(ChannelMonitor(dbSample[0]))
channelList.append(ChannelMonitor(dbSample[1]))

channelList[0].channel.subscribe(channelList[0].info['pvname'], channelList[0].monitor)
channelList[1].channel.subscribe(channelList[1].info['pvname'], channelList[1].monitor)

channelList[0].channel.startMonitor()
channelList[1].channel.startMonitor()

current_time = int(time.time())
print('current time', current_time)
time.sleep(20)

print('unsubscribe channel1')
channelList[0].channel.unsubscribe(channelList[0].info['pvname'])

current_time = int(time.time())
print('current time', current_time)

time.sleep(20)
# c.subscribe('echo', echo)
# c.startMonitor()

# @app.route('/', methods=['GET'])
# def test():
    # return "OK"

# if __name__ == "__main__":
    # app.run(host=SERVER_ADDR, port="8000")