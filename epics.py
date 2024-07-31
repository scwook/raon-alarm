from pvaccess import *
import time
# from flask import Flask

# app = Flask(__name__)

SERVER_ADDR = 'localhost'

dbSample = [
    {'pvname':'scwook:ai1', 'value':5.0, 'condition':0, 'state':'normal', 'active':True, 'lasttime': '0', 'repeat':0},
    {'pvname':'scwook:ai2', 'value':5.0, 'condition':0, 'state':'normal', 'active':False, 'lasttime': '0', 'repeat':0}
    ]

def valueCompare(referenceValue, comparisonValue, operator):
    if operator == 0:
        return (referenceValue == comparisonValue)

    elif operator == 1:
        return (referenceValue > comparisonValue)
    
    elif operator == 2:
        return (referenceValue < comparisonValue)

    else:
        return None

class ChannelMonitor:
    def __init__(self, info):
        self.alarmInfo = info
        self.channel = Channel(info['pvname'], ProviderType.CA)

    def monitor(self, channelData):
        recordData = dict(channelData)
        alarmValue = self.alarmInfo['value']
        alarmState = self.alarmInfo['state']
        alarmActive = self.alarmInfo['active']

        if recordData['value'] > alarmValue:
            if alarmActive and alarmState == 'normal':
                print(self.alarmInfo['pvname'], 'alarm')
                self.alarmInfo['state'] = 'alarm'
                self.alarmInfo['timestamp'] = int(time.time())
            else:
                print(self.alarmInfo['pvname'], 'alarm deactive')


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