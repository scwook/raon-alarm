import datetime
import time
import sql
import epics
import json
import serial
import multiprocessing
import queue
import logging

from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

# SERVER_ADDR = 'localhost'
SERVER_ADDR = '192.168.131.161'
# SERVER_ADDR = '192.168.150.219'

app = Flask(__name__)
CORS(app)

log=logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# conn = sql.getDbConnection()
# alarmList = sql.getAlarmList()
channelList = list()
# monitoringList = list()

def restartMonitoring(pvname):
    for y in channelList:
        if y.pvname == pvname:
            y.channel.stopMonitor()
            
            # if not y.timer == None and y.timer.is_alive():
            #     y.timer.cancel()

            y.channel.startMonitor('field(value)')
            break

def stopMonitoring(pvname):
    for y in channelList:
        if y.pvname == pvname:
            y.channel.stopMonitor()
            print(pvname, "stop monitor")

def startMonitoring(pvname):
    for y in channelList:
        if y.pvname == pvname:
            if not y.channel.isMonitorActive():
                y.channel.stopMonitor()

            # if not y.timer == None and y.timer.is_alive():
            #     y.timer.cancel()

            y.channel.startMonitor('field(value)')
            break

def deleteMonitoring(pvname):
    for y in channelList:
        if y.pvname == pvname:
            if y.channel.isMonitorActive():
                y.channel.stopMonitor()

            if y.timer != None:
                y.timer.cancel()

            channelList.remove(y)
            break

# def checkAlarmRepeat(pvname):
#     for y in channelList:
#         if y.pvname == pvname:
#             if not y.timer == None and not y.timer.is_alive():
#                 alarmInfo = sql.getAlarmListFromPV(pvname)[0]
#                 repeatTime = int(alarmInfo['repetation'])
#                 y.alarmRepeat(repeatTime)

def checkInitState(ch):
    pvname = ch.pvname
    alarmInfo = sql.getAlarmListFromPV(pvname)[0]
    alarmState = alarmInfo['state']
    repeatTime = alarmInfo['repetation']

    if alarmState == 'normal' :
        ch.channel.startMonitor('field(value)')
        print(pvname, ': start monitoring')

    else:
        repeatTime = alarmInfo['repetation']
        ch.alarmRepeat(repeatTime)
        print(pvname, ': start alarm repeat')
        

def connectionStateAll():
    stateList = list()
    for y in channelList:
        state = y.channel.isConnected()
        pvname = y.pvname
        stateList.append({'pvname':pvname, 'state':state})

    return stateList

def writeErrorLog(message, error):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = '\n' + now + ' ' + message
    error = '\n' + now + ' ' + str(error)

    with open('error.log', 'a', encoding='utf-8') as file:
        file.write(message)
        file.write(error)


@app.route('/', methods=['POST'])
def test():
    formData = request.form
    print(formData)
    return "OK"

@app.route('/updateAlarmInfo', methods=['POST'])
def updateAlarmInfo():
    jsonData = request.get_json()
    pvname = jsonData['pvname']
    description = jsonData['desc']
    value = jsonData['value']
    operator = int(jsonData['condition'])
    delay = int(jsonData['delay'])
    repetation = int(jsonData['repetation']) * 60
    sms = jsonData['phone']

    recordData = {'pvname':pvname, 'description':description, 'value':value, 'operator':operator, 'dealy':delay, 'repetation':repetation, 'sms':sms}

    result = sql.updateAlarmInfo(recordData)
    if result == 'OK':
        sql.insertAlarmLog(pvname, 'Update alarm info: %s' % (jsonData))
        # checkAlarmRepeat(pvname)
        restartMonitoring(pvname)

    else:
        message = '(updateAlarmInfo) %s %' % (jsonData)
        writeErrorLog(message, result)

    return result

@app.route('/insertAlarmInfo', methods=['POST'])
def insertAlarmInfo():
    jsonData = request.get_json()
    pvname = jsonData['pvname'].strip()
    description = jsonData['desc']
    value = jsonData['value']
    operator = int(jsonData['condition'])
    state = 'normal'
    activation = bool(1)
    delay = int(jsonData['delay'])
    repetation = int(jsonData['repetation']) * 60
    sms = jsonData['phone']

    recordData = {'pvname':pvname, 'description':description, 'value':value, 'operator':operator, 'state': state, 'activation': activation, 'dealy':delay, 'repetation':repetation, 'sms':sms}

    result = sql.insertAlarmInfo(recordData)

    if result == 'OK':
        channelClass = epics.ChannelMonitor(pvname)
        channelList.append(channelClass)
        channelClass.channel.subscribe(pvname, channelClass.alarmMonitor)
        channelClass.channel.startMonitor('field(value)')

        sql.insertAlarmLog(pvname, 'Create new alarm monitoring')

    else:
        message = '(insertAlarmInfo) %s %' % (jsonData)
        writeErrorLog(message, result)

    return result

@app.route('/getAlarmListFromPV/<pvname>', methods=['GET'])
def getAlarmListFromPV(pvname):
    sqlWildcardString = pvname.replace('*', '%')
    result = sql.getAlarmListFromPV(sqlWildcardString)

    return json.dumps(result, ensure_ascii=False)

@app.route('/getAlarmListFromPhone/<phone>', methods=['GET'])
def getAlarmListFromPhone(phone):
    # sqlWildcardString = phone.replace('*', '%')
    result = sql.getAlarmListFromPhone(phone)

    return json.dumps(result, ensure_ascii=False)

@app.route('/updateAlarmField', methods=['POST'])
def setUpdateAlarmField():
    jsonData = request.get_json()
    pvname = jsonData['pvname']
    field = jsonData['field']
    value = jsonData['value']

    if field == 'pvname':
        result = sql.updateAlarmFieldStr(pvname, field, value)
        if result == 'OK':
            sql.insertAlarmLog(pvname, 'Update PV name to %s' % (value))

    elif field == 'description' or field == 'value':
        result = sql.updateAlarmFieldStr(pvname, field, value)

    elif field == 'state':
        result = sql.updateAlarmFieldStr(pvname, field, value)
        if result == 'OK':
            restartMonitoring(pvname)
            sql.insertAlarmLog(pvname, 'Change alarm state to %s' % (value))

    elif field == 'operator' or field == 'repetation' or field == 'delay':
        value = int(value)
        result = sql.updateAlarmFieldInt(pvname, field, value)
        if result == 'OK':
            sql.insertAlarmLog(pvname, 'Change condition to %s' % (value))

    elif field == 'activation':
        value = bool(value)
        result = sql.updateAlarmFieldInt(pvname, field, value)
        if result == 'OK':
            # if value:
            #     startMonitoring(pvname)
            # else:
            #     stopMonitoring(pvname)

            sql.insertAlarmLog(pvname, 'Change activation to %s' % (value))

    else:
        result = 'Field name error'

    if result != 'OK':
        message = '(updateAlarmField) pvname:%s, field:%s, value:%s' % (pvname, field, value) 
        writeErrorLog(message, result)

    return result

@app.route('/smsInfoUpdate', methods=['POST'])
def setSMSInfoUpdate():
    jsonData = request.get_json()
    phone = jsonData['phone']
    pvname = jsonData['pvname']
    field = jsonData['field']
    value = jsonData['value']

    result = sql.updateSMSFieldInt(phone, pvname, field, value)
    if result == 'OK':
            return 'OK'

    else:
        message = '(smsInfoUpdate) %s %' % (jsonData)
        writeErrorLog(message, result)

    return result

@app.route('/get', methods=['GET'])
def getData():
    result = sql.getAlarmList()

    return json.dumps(result, ensure_ascii=False)


@app.route('/clear', methods=['POST'])
def clearAlarm():
    sql.clearAlarm()

    for x in channelList:
        x.alarmInfo['state'] = 'normal'

    return "OK"

@app.route('/getAlarmListAll', methods=['GET'])
def getAlarmListAll():
    result = sql.getAlarmListAll()

    return json.dumps(result, ensure_ascii=False)

@app.route('/getAlarmStateAll', methods=['GET'])
def getAlarmStateAll():
    result = sql.getAlarmStateAll()

    return json.dumps(result, ensure_ascii=False)

@app.route('/getConnectionStateAll', methods=['GET'])
def getConnectionStateAll():
    result = connectionStateAll()

    return json.dumps(result, ensure_ascii=False)

@app.route('/deleteAlarmInfo/<pvname>', methods=['GET'])
def deleteAlarmInfo(pvname):
    result  = sql.deleteAlarmInfo(pvname)
    
    if result == 'OK':
        deleteMonitoring(pvname)
        sql.insertAlarmLog(pvname, 'Delete alarm monitoring')
    else:
        writeErrorLog(result)

    return result

@app.route('/deleteSMSInfo', methods=['POST'])
def deleteSMSInfo():
    jsonData = request.get_json()
    phone = jsonData['phone']
    pvname = jsonData['pvname']
    sql.deleteSMSList(phone, pvname)

    return 'OK'

PORT = '/dev/tty.usbserial-FT96QAFW'
ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)

def sendMessage(q):
    while True:
        try:
            data = q.get(block=False)
            ser.write(data.encode('utf-8') + b'\r\n')
            print('sned data: ' + data)

        except queue.Empty:
            pass

        time.sleep(0.1)    

if __name__ == "__main__":
    q = multiprocessing.Queue()

    for alarmlist in sql.getAlarmList():
        channelList.append(epics.ChannelMonitor(alarmlist['pvname'], q))

    for channelMonitor in channelList:
        channelMonitor.channel.subscribe(channelMonitor.pvname, channelMonitor.alarmMonitor)
        # checkInitState(channelMonitor)
        channelMonitor.channel.startMonitor('field(value)')

    process = multiprocessing.Process(target=sendMessage, args={q})
    process.start()
    # process.join()

    app.run(host=SERVER_ADDR, port="8000")