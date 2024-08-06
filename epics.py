import threading
from pvaccess import *

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


# channelList[1].channel.startMonitor()

# current_time = int(time.time())
# print('current time', current_time)
# time.sleep(20)

# print('unsubscribe channel1')
# channelList[0].channel.unsubscribe(channelList[0].alarmInfo['pvname'])

# current_time = int(time.time())
# print('current time', current_time)

