import threading
import sql
import serial
from pvaccess import *
import time
import clue

class ChannelMonitor:
    def __init__(self, pvname, queue):
        # self.alarmInfo = info
        # self.channel = Channel(info['pvname'], CA)
        self.pvname = pvname
        self.channel = Channel(pvname, CA)
        self.valueType = None
        self.timer = None
        self.messageQueue = queue

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

        return valueType

    def alarmMonitor(self, channelData):
        recordData = dict(channelData)
        alarmInfo = sql.getAlarmListFromPV(self.channel.getName())[0]
        alarmState = alarmInfo['state']
        alarmActivation = alarmInfo['activation']
        pvNmae = alarmInfo['pvname']

        # in case of alarm activation value 0, not going to alarm sequence
        # if not alarmActivation:
            # clue.printConsole(pvNmae, 'alarm activation fasle')
            # return
        
        ###########################################
        # If currently in alarm state, start repeat loop
        #
        if alarmState == 'alarm':
            if not self.timer == None and self.timer.is_alive():
                self.timer.cancel()
        
            repeatTime = int(alarmInfo['repetation'])
            if repeatTime == 0:
                clue.printConsole(pvNmae, 'already alarm raised no repeat')
                return
            
            self.channel.stopMonitor()

            clue.printConsole(pvNmae, 'start repeat loop')
            self.timer = threading.Timer(repeatTime, self.alarmRepeat, args=[repeatTime])
            self.timer.start()
            return

        ###########################################
        # If currently in not alarm state, check alarm condition and start alarm loop
        #

        valueType = self.valueType
        
        # check value type for type conversion and comapre value
        if valueType == None:
            valueType = self.checkValueType(recordData)

        pvValue = recordData['value']
        alarmValue = alarmInfo['value']
        operator = int(alarmInfo['operator'])

        # check alarm condition
        result = valueCompare(pvValue, alarmValue, operator, valueType)
 
        # just ignore when alarm conditions are not met
        if not result:
            clue.printConsole(pvNmae, 'no alarm')
            return
        
        clue.printConsole(pvNmae, 'stop monitoring and start delay timer')

        self.channel.stopMonitor()
        delayTime = int(alarmInfo['delay'])

        timer = threading.Timer(delayTime, self.alarmDelay, args=[alarmInfo])
        timer.start()

        # when alarm conditions are met, check current alarm state
        # if alarmState == 'normal':
        #     clue.printConsole(pvNmae, 'stop monitoring and start delay timer')

        #     self.channel.stopMonitor()
        #     delayTime = int(alarmInfo['delay'])

        #     timer = threading.Timer(delayTime, self.alarmDelay, args=[alarmInfo])
        #     timer.start()

        # elif alarmState == 'alarm':
        #     if not self.timer == None and self.timer.is_alive():
        #         self.timer.cancel()
        
        #     repeatTime = int(alarmInfo['repetation'])
        #     if repeatTime == 0:
        #         clue.printConsole(pvNmae, 'already alarm raised no repeat')
        #         return
            
        #     self.channel.stopMonitor()

        #     clue.printConsole(pvNmae, 'start repeat loop')
        #     self.timer = threading.Timer(repeatTime, self.alarmRepeat, args=[repeatTime])
        #     self.timer.start()
            
        # else:
        #     clue.printConsole(pvNmae, 'alarm state error')

    def alarmDelay(self, alarmInfo):
        pvName = alarmInfo['pvname']

        if self.channel.isConnected() == False:
            clue.printConsole(pvName, 'channel disconnected')
            self.channel.startMonitor()
            return
        
        pvValue = self.channel.get().toDict()['value']
        alarmValue = alarmInfo['value']
        operator = int(alarmInfo['operator'])
        alarmActivation = alarmInfo['activation']
        valueType = self.valueType
        result = valueCompare(pvValue, alarmValue, operator, valueType)

        if result and alarmActivation:
            # channelClass.alarmInfo['state'] = 'alarm'
            # pvName = alarmInfo['pvname']
            alarmLog = 'alarm raised'
            
            self.updateAlarmFieldStr(pvName, 'state', 'alarm')
            self.writeAlarmLog(pvName, alarmLog)
            
            # message = {"desc":alarmInfo['description'], "value":alarmInfo['value'], "list":alarmInfo['sms']}
            message = {"desc":alarmInfo['description'], "value":str(pvValue), "list":alarmInfo['sms']}

            self.messageQueue.put(str(message))

            clue.printConsole(pvName, 'alarm raised')
        else:
            clue.printConsole(pvName, 'alarm delay overtime')

        self.channel.startMonitor()
        clue.printConsole(pvName, 'restart monitoring')

    def alarmRepeat(self, repeatTime):

        if not self.channel.isConnected():
            clue.printConsole(self.pvname, 'channel disconnected')
            # self.channel.startMonitor()
            return

        alarmInfo = sql.getAlarmListFromPV(self.channel.getName())[0]
        pvName = alarmInfo['pvname']
        pvValue = self.channel.get().toDict()['value']
        alarmState = alarmInfo['state']
        alarmActivation = alarmInfo['activation']
        repeat = alarmInfo['repetation']

        clue.printConsole(pvName, 'start repeat')
        self.timer = threading.Timer(repeatTime, self.alarmRepeat, args=[repeat])
        self.timer.start()
        # print('start', self.timer)
        # print('alive', self.timer.is_alive())

        if alarmState == 'alarm' and alarmActivation:
            # pvName = alarmInfo['pvname']
            alarmLog = 'alarm raised'
            
            self.writeAlarmLog(pvName, alarmLog)
            # sendAlarmSMS()
            # message = {"desc":alarmInfo['description'], "value":alarmInfo['value'], "list":alarmInfo['sms']}
            message = {"desc":alarmInfo['description'], "value":str(pvValue), "list":alarmInfo['sms']}

            self.messageQueue.put(str(message))

        if alarmState == 'normal' or repeat == 0:
            self.timer.cancel()
            self.channel.startMonitor()
            # print('stop', self.timer)
            # print('alive', self.timer.is_alive())

            # pvName = alarmInfo['pvname']
            clue.printConsole(pvName, 'stop alarm repeat and start monitoring')

    def updateAlarmFieldStr(self, pvname, field, value):
        sql.updateAlarmFieldStr(pvname, field, value)

    def writeAlarmLog(self, pvname, log):
        sql.insertAlarmLog(pvname, log)

# def sendAlarmSMS():
#     print('alarm send')

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