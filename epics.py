from pvaccess import *
import time
import asyncio
import threading
from flask import Flask

app = Flask(__name__)

SERVER_ADDR = 'localhost'

dbPhone = ['01048792718']

dbSample = [
    {'pvname':'scwook:ai1', 'value':5.0, 'operator':1, 'state':'normal', 'activation':True, 'lasttime': '0', 'repeat':10, 'delay': 2},
    {'pvname':'scwook:ai2', 'value':5.0, 'operator':1, 'state':'normal', 'activation':False, 'lasttime': '0', 'repeat':0, 'delay': 2}
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

def alarmDelay(channelClass):
    pvValue = channelClass.channel.get().toDict()['value']
    alarmValue = channelClass.alarmInfo['value']
    operator = int(channelClass.alarmInfo['operator'])
    result = valueCompare(pvValue, alarmValue, operator)

    if result:
        channelClass.alarmInfo['state'] = 'alarm'
        sendAlarmSMS()
        print('     ', channelClass.alarmInfo['pvname'], 'alarm raised')
    else:
        print('     overtime alarm')

    channelClass.channel.startMonitor()
    print('     restart monitoring')

def alarmRepeat(repeatTime, channelClass):
    alarmState = channelClass.alarmInfo['state']
    timer = threading.Timer(repeatTime, alarmRepeat, args=[repeatTime, channelClass])
    timer.start()

    if alarmState == 'alarm':
        sendAlarmSMS()
    else:
        timer.cancel()
        channelClass.channel.startMonitor()
        print('     stop alarm repeat and start monitoring')

def sendAlarmSMS():
    print('alarm send')

class ChannelMonitor:
    def __init__(self, info):
        self.alarmInfo = info
        self.channel = Channel(info['pvname'], ProviderType.CA)

    def alarmMonitor(self, channelData):
        recordData = dict(channelData)

        alarmState = self.alarmInfo['state']
        alarmActivation = self.alarmInfo['activation']
        print(self.alarmInfo['pvname'], recordData['value'])
        
        if alarmActivation:
            pvValue = recordData['value']
            alarmValue = self.alarmInfo['value']
            operator = int(self.alarmInfo['operator'])

            result = valueCompare(pvValue, alarmValue, operator)
            if result:
                if alarmState == 'normal':
                    print('stop monitoring and start timer')

                    self.channel.stopMonitor()
                    delayTime = int(self.alarmInfo['delay'])

                    timer = threading.Timer(delayTime, alarmDelay, args=[self])
                    timer.start()

                elif alarmState == 'alarm':
                    repeatTime = int(self.alarmInfo['repeat'])
                    if repeatTime != 0:
                        self.channel.stopMonitor()
                        timer = threading.Timer(repeatTime, alarmRepeat, args=[repeatTime, self])
                        timer.start()
                    
                    else:
                        print('already alarm raise no repeat')

channelList = list()
monitoringList = list()

channelList.append(ChannelMonitor(dbSample[0]))
channelList.append(ChannelMonitor(dbSample[1]))

channelList[0].channel.subscribe(channelList[0].alarmInfo['pvname'], channelList[0].alarmMonitor)
channelList[1].channel.subscribe(channelList[1].alarmInfo['pvname'], channelList[1].alarmMonitor)

channelList[0].channel.startMonitor()
# channelList[1].channel.startMonitor()

# current_time = int(time.time())
# print('current time', current_time)
# time.sleep(20)

# print('unsubscribe channel1')
# channelList[0].channel.unsubscribe(channelList[0].alarmInfo['pvname'])

# current_time = int(time.time())
# print('current time', current_time)

@app.route('/', methods=['GET'])
def test():
    return "OK"

if __name__ == "__main__":
    app.run(host=SERVER_ADDR, port="8000")