import threading
import sql
from pvaccess import *
import time

class ChannelMonitor:
    def __init__(self, pvname):
        # self.alarmInfo = info
        # self.channel = Channel(info['pvname'], CA)
        self.pvname = pvname
        self.channel = Channel(pvname, CA)
        self.valueType = None
        self.timer = None

    def checkValueType(self, data):
        # print(self.channel.isConnected())
        valueType = None

        if self.channel.isConnected():
            # typeDefinitionDic = self.channel.getIntrospectionDict()
            # print(self.channel.get('field(value)'))
            # valueType = str(typeDefinitionDic['value'])
            value = data['value']
            if isinstance(value, float):
                valueType = 'FLOAT'
            elif isinstance(value, int):
                valueType = 'INT'
            elif isinstance(value, bool):
                valueType = 'BOOLEAN'
            else:
                if isinstance(value, dict):
                    valueType = 'ENUM'
                else:
                    valueType = None

        self.valueType = valueType

        print('value type', valueType)
        return valueType

    def alarmMonitor(self, channelData):
        recordData = dict(channelData)
        print(channelData)
        alarmInfo = sql.getAlarmListFromPV(self.channel.getName())[0]
        alarmState = alarmInfo['state']
        alarmActivation = alarmInfo['activation']
        if alarmActivation:
            pvValue = recordData['value']
            alarmValue = alarmInfo['value']
            operator = int(alarmInfo['operator'])
            valueType = self.valueType
            if valueType == None:
                valueType = self.checkValueType(recordData)

            result = valueCompare(pvValue, alarmValue, operator, valueType)
            if result:
                if alarmState == 'normal':
                    print('stop monitoring and start timer')

                    self.channel.stopMonitor()
                    delayTime = int(alarmInfo['delay'])

                    timer = threading.Timer(delayTime, alarmDelay, args=[alarmInfo, self])
                    timer.start()

                elif alarmState == 'alarm':
                    repeatTime = int(alarmInfo['repetation'])
                    if repeatTime != 0:
                        self.channel.stopMonitor()
                        timer = threading.Timer(repeatTime, alarmRepeat, args=[repeatTime, alarmInfo, self])
                        timer.start()
                    
                    else:
                        print('already alarm raise no repeat')
                
                else:
                    print('alarm state error')

            else:
                print('No alarm')
        else:
            print('alarm activation false')

def valueCompare(referenceValue, comparisonValue, operator, valueType):
    if valueType == 'DOUBLE' or valueType == 'FLOAT':
        referenceValue = float(referenceValue)
        comparisonValue = float(comparisonValue)

    elif valueType == 'INT':
        referenceValue = int(referenceValue)
        comparisonValue = int(comparisonValue)

    elif valueType == 'BOOLEAN':
        referenceValue == bool(referenceValue)
        comparisonValue == bool(comparisonValue)
    elif valueType == 'ENUM':
        referenceValue = int(referenceValue['index'])
        comparisonValue = int(comparisonValue)

    if operator == 0:
        return (referenceValue == comparisonValue)

    elif operator == 1:
        return (referenceValue < comparisonValue)
    
    elif operator == 2:
        return (referenceValue > comparisonValue)
    
    elif operator == 3:
        return (referenceValue != comparisonValue)
    
    elif operator == 4:
        return (referenceValue <= comparisonValue)
    
    elif operator == 5:
        return (referenceValue >= comparisonValue)

    else:
        return None

def alarmDelay(alarmInfo, channelClass):
    pvValue = channelClass.channel.get().toDict()['value']
    alarmValue = alarmInfo['value']
    operator = int(alarmInfo['operator'])
    alarmActivation = alarmInfo['activation']
    valueType = channelClass.valueType
    result = valueCompare(pvValue, alarmValue, operator, valueType)

    if result and alarmActivation:
        # channelClass.alarmInfo['state'] = 'alarm'
        pvName = alarmInfo['pvname']
        alarmLog = 'alarm raised'
        
        updateAlarmFieldStr(pvName, 'state', 'alarm')
        writeAlarmLog(pvName, alarmLog)
        sendAlarmSMS()
        print('     ', alarmInfo['pvname'], 'alarm raised')
    else:
        print('     overtime alarm')

    channelClass.channel.startMonitor()
    print('     restart monitoring')

def alarmRepeat(repeatTime, alarmInfo, channelClass):
    alarmState = alarmInfo['state']
    alarmActivation = alarmInfo['activation']

    channelClass.timer = threading.Timer(repeatTime, alarmRepeat, args=[repeatTime, alarmInfo, channelClass])
    channelClass.timer.start()

    if alarmState == 'alarm' and alarmActivation:
        pvName = alarmInfo['pvname']
        alarmLog = 'alarm raised'
        
        # writeAlarmLog(pvName, alarmLog)
        sendAlarmSMS()
    else:
        channelClass.timer.cancel()
        channelClass.channel.startMonitor()
        print('     stop alarm repeat and start monitoring')

def updateAlarmFieldStr(pvname, field, value):
    # conn = sql.getDbConnection()
    sql.updateAlarmFieldStr(pvname, field, value)

def writeAlarmLog(pvname, log):
    conn = sql.getDbConnection()
    # sql.insertAlarmLog(pvname, log)

def sendAlarmSMS():
    print('alarm send')

# channelList[1].channel.startMonitor()

# current_time = int(time.time())
# print('current time', current_time)
# time.sleep(20)

# print('unsubscribe channel1')
# channelList[0].channel.unsubscribe(channelList[0].alarmInfo['pvname'])

# current_time = int(time.time())
# print('current time', current_time)

