# system library
# import datetime
import time
import multiprocessing
import queue
import logging
import asyncio
import threading
import os
import ast
from datetime import datetime

# extenstion library
import json
import serial

from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

# user library
import sql
import epics
import clue

# websocket librarys
import websockets

# EPICS Addr list
kobra_addr = '192.168.131.27'
ndps_addr = '192.168.135.27'
cls_addr = '192.168.150.197'
addr_list = f'{kobra_addr} {ndps_addr} {cls_addr}'
os.environ['EPICS_CA_ADDR_LIST'] = addr_list
os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'

# SERVER_ADDR = 'localhost'
SERVER_ADDR = '192.168.131.194'
REST_PORT = 9009
WEBSOCKET_PORT = 9010
# SERVER_ADDR = '192.168.150.219'

app = Flask(__name__)
CORS(app)

log=logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

connected_clients = set()
main_loop = None

# conn = sql.getDbConnection()
# alarmList = sql.getAlarmList()
channelList = list()
# monitoringList = list()

q = multiprocessing.Queue()


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

# def writeErrorLog(message, error):
#     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     message = '\n' + now + ' ' + message
#     error = '\n' + now + ' ' + str(error)

#     with open('error.log', 'a', encoding='utf-8') as file:
#         file.write(message)
#         file.write(error)

def checkInvalidValue(data):
    try:
        int(data['condition'])
        int(data['delay'])
        int(data['repetation'])

        for x in data['phone']:
            int(x)

        return 'OK'
    except ValueError as e:
        return e

def checkPVName(pvname):
    result = sql.getAlarmListFromPV(pvname)
    if len(result):
        return False

    return True

# --------------------------
# WebSocket Server
# --------------------------
async def ws_handler(ws):
    connected_clients.add(ws)
    client_ip, client_port = ws.remote_address
    message = f'{client_ip} connection websocket'
    clue.writeMessageLog(message)
    clue.printConsole(message)
    try:
        async for msg in ws:
            message = f'{client_ip} websocket received {msg}'
            clue.printConsole(message)
    finally:
        connected_clients.remove(ws)
        message = f'{client_ip} disconnection websocke'
        clue.writeMessageLog(message)
        clue.printConsole(message)


async def ws_server():
    async with websockets.serve(ws_handler, SERVER_ADDR, WEBSOCKET_PORT):
        clue.printConsole(f"[WebSocket] server started on {WEBSOCKET_PORT}")
        await asyncio.Future()  # forever

async def ws_broadcast(message):
    clue.printConsole(f"[Websocket] broadcast sending {message}")
    if connected_clients:
        await asyncio.gather(*(client.send(json.dumps(message)) for client in connected_clients))
    else:
        clue.printConsole("[WebSocket] no clients connected")

# --------------------------
# Flask Server
# --------------------------
@app.route('/', methods=['POST'])
def test():
    # formData = request.form
    # print(formData)
    return "OK"

@app.route('/updateAlarmInfo', methods=['POST'])
def updateAlarmInfo():
    jsonData = request.get_json()

    result = checkInvalidValue(jsonData)
    if result != 'OK':
        message = f'{request.remote_addr} [ERROR] (updateAlarmInfo) {result} {jsonData}'
        # clue.writeErrorLog(message, result)
        clue.writeMessageLog(message)
        clue.printConsole(message)
        return 'Invalid Value'

    pvname = jsonData['pvname']
    description = jsonData['desc']
    value = jsonData['value']
    operator = int(jsonData['condition'])
    delay = int(jsonData['delay'])
    repetation = int(jsonData['repetation']) * 60
    sms = jsonData['phone']

    recordData = {'pvname':pvname, 'description':description, 'value':value, 'operator':operator, 'dealy':delay, 'repetation':repetation, 'sms':sms}

    result = sql.updateAlarmInfo(recordData)
    if result != 'OK':
        message = f'{request.remote_addr} [ERROR] (updateAlarmInfo) {result} {jsonData}'
        clue.writeMessageLog(message)
        clue.printConsole(message)
        return result

    sql.insertAlarmLog(pvname, 'Update alarm info: %s' % (jsonData))
    # checkAlarmRepeat(pvname)
    restartMonitoring(pvname)

    message = f'{request.remote_addr} [MESSAGE] (updateAlarmInfo) update alarm info {jsonData}'
    clue.writeMessageLog(message)
    clue.printConsole(message)

    global main_loop
    brocast_data = {**recordData, 'delay':jsonData['delay'], 'field':'update'}
    main_loop.call_soon_threadsafe(asyncio.create_task, ws_broadcast(brocast_data))

    return result

@app.route('/insertAlarmInfo', methods=['POST'])
def insertAlarmInfo():
    jsonData = request.get_json()

    pvname = jsonData['pvname'].strip()
    result = checkPVName(pvname)
    if not result:
        message = f'{request.remote_addr} [ERROR] pv already exists (insertAlarmInfo) {jsonData}'
        clue.writeMessageLog(message)
        clue.printConsole(message)

        return 'Invalid PV'

    result = checkInvalidValue(jsonData)
    if result != 'OK':
        # message = '(insertAlarmInfo) %s' % (jsonData)
        # clue.writeErrorLog(message, result)
        message = f'{request.remote_addr} [ERROR] (insertAlarmInfo) {result} {jsonData}'
        clue.writeMessageLog(message)
        clue.printConsole(message)
        return 'Invalid Value'
    
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

    if result != 'OK':
        message = f'{request.remote_addr} [ERROR] {result} (insertAlarmInfo) {jsonData}'
        clue.writeMessageLog(message)
        clue.printConsole(message)
        return result


    channelClass = epics.ChannelMonitor(pvname, q)
    channelList.append(channelClass)
    channelClass.channel.subscribe(pvname, channelClass.alarmMonitor)
    channelClass.channel.startMonitor('field(value)')

    sql.insertAlarmLog(pvname, 'Create new alarm monitoring')

    message = f'{request.remote_addr} [MESSAGE] (insertAlarmInfo) create new alarm monitoring {jsonData}'
    clue.writeMessageLog(message)
    clue.printConsole(message)

    global main_loop
    brocast_data = {**recordData, 'delay':jsonData['delay'], 'field':'create'}
    main_loop.call_soon_threadsafe(asyncio.create_task, ws_broadcast(brocast_data))

    return result

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
        clue.writeErrorLog(message, result)
    else:
        global main_loop
        brocast_data = {'pvname':pvname, 'field':field, 'value':value}
        main_loop.call_soon_threadsafe(asyncio.create_task, ws_broadcast(brocast_data))

    return result

@app.route('/smsInfoUpdate', methods=['POST'])
def setSMSInfoUpdate():
    jsonData = request.get_json()
    phone = jsonData['phone']
    pvname = jsonData['pvname']
    field = jsonData['field']
    value = jsonData['value']

    result = sql.updateSMSFieldInt(phone, pvname, field, value)
    
    if result != 'OK':
        message = f'{request.remote_addr} [ERROR] (smsInfoUpdate) {jsonData}'
        clue.writeMessageLog(message)
        clue.printConsole(message)
        return result

    sql.insertAlarmLog(pvname, 'Update sms info')

    message = f'{request.remote_addr} [MESSAGE] (smsInfoUpdate) update sms info {jsonData}'
    clue.writeMessageLog(message)
    clue.printConsole(message)

    global main_loop
    brocast_data = {'phone': phone, 'pvname':pvname, 'field':field, 'value':value}
    main_loop.call_soon_threadsafe(asyncio.create_task, ws_broadcast(brocast_data))

    return result

# @app.route('/get', methods=['GET'])
# def getData():
#     result = sql.getAlarmList()

#     return json.dumps(result, ensure_ascii=False)


# @app.route('/clear', methods=['POST'])
# def clearAlarm():
#     sql.clearAlarm()

#     for x in channelList:
#         x.alarmInfo['state'] = 'normal'

#     return "OK"

@app.route('/getAlarmListAll', methods=['GET'])
def getAlarmListAll():
    result, data = sql.getAlarmListAll()

    if result != 'OK':
        message = f'{request.remote_addr} [ERROR] (getAlarmListAll) {data}'
        clue.writeMessageLog(message)
        clue.printConsole(message)
        return result

    message = f'{request.remote_addr} [MESSAGE] (getAlarmListAll) get alarm list all'
    clue.writeMessageLog(message)
    clue.printConsole(message)

    return json.dumps(data, ensure_ascii=False)

@app.route('/getAlarmStateAll', methods=['GET'])
def getAlarmStateAll():
    result, data = sql.getAlarmStateAll()

    if result != 'OK':
        message = f'{request.remote_addr} [ERROR] (getAlarmStateAll) {data}'
        # clue.writeMessageLog(message)
        # clue.printConsole(message)
        return result
    
    message = f'{request.remote_addr} [MESSAGE] (getAlarmStateAll) get alarm state all'
    # clue.writeMessageLog(message)
    # clue.printConsole(message)

    return json.dumps(data, ensure_ascii=False)

@app.route('/getConnectionStateAll', methods=['GET'])
def getConnectionStateAll():
    data = connectionStateAll()

    return json.dumps(data, ensure_ascii=False)

@app.route('/getAlarmListFromPV/<pvname>', methods=['GET'])
def getAlarmListFromPV(pvname):
    sqlWildcardString = pvname.replace('*', '%')
    result, data = sql.getAlarmListFromPV(sqlWildcardString)

    if result != 'OK':
        message = f'{request.remote_addr} [ERROR] (getAlarmListFromPV) {data}'
        clue.writeMessageLog(message)
        clue.printConsole(message)

        return result
        
    message = f'{request.remote_addr} [MESSAGE] (getAlarmListFromPV) get alarm list from pv {pvname}'
    clue.writeMessageLog(message)
    clue.printConsole(message)

    return json.dumps(data, ensure_ascii=False)

@app.route('/getAlarmListFromPhone/<phone>', methods=['GET'])
def getAlarmListFromPhone(phone):
    # sqlWildcardString = phone.replace('*', '%')
    result, data = sql.getAlarmListFromPhone(phone)

    if result != 'OK':
        message = f'{request.remote_addr} [ERROR] (getAlarmListFromPhone) {data}'
        clue.writeMessageLog(message)
        clue.printConsole(message)

        return result

    message = f'{request.remote_addr} [MESSAGE] (getAlarmListFromPhone) get alarm list from phone {phone}'
    clue.writeMessageLog(message)
    clue.printConsole(message)

    return json.dumps(data, ensure_ascii=False)

@app.route('/deleteAlarmInfo/<pvname>', methods=['GET'])
def deleteAlarmInfo(pvname):
    result  = sql.deleteAlarmInfo(pvname)
    
    if result != 'OK':
        message = f'{request.remote_addr} [ERROR] (deleteAlarmInfo) {pvname}'
        clue.writeMessageLog(message)
        clue.printConsole(message)
        return result

    deleteMonitoring(pvname)
    sql.insertAlarmLog(pvname, 'Delete alarm monitoring')

    message = f'{request.remote_addr} [MESSAGE] (deleteAlarmInfo) delete alarm monitoring {pvname}'
    clue.writeMessageLog(message)
    clue.printConsole(message)

    global main_loop
    brocast_data = {'pvname':pvname, 'field':'delete'}
    main_loop.call_soon_threadsafe(asyncio.create_task, ws_broadcast(brocast_data))

    return result

@app.route('/deleteSMSInfo', methods=['POST'])
def deleteSMSInfo():
    jsonData = request.get_json()
    phone = jsonData['phone']
    pvname = jsonData['pvname']
    result = sql.deleteSMSList(phone, pvname)

    if result != 'OK':
        message = f'{request.remote_addr} [ERROR] (deleteSMSInfo) {pvname}'
        clue.writeMessageLog(message)
        clue.printConsole(message)
        return result

    message = f'{request.remote_addr} [MESSAGE] (deleteSMSInfo) delete sms info {pvname}'
    clue.writeMessageLog(message)
    clue.printConsole(message)

    global main_loop
    brocast_data = {'phone':phone, 'pvname':pvname, 'field':'delete'}
    main_loop.call_soon_threadsafe(asyncio.create_task, ws_broadcast(brocast_data))
    
    return result

def run_flask():
    app.run(host=SERVER_ADDR, port=REST_PORT)

# --------------------------
# Serial Server
# --------------------------
PORT = '/dev/ttyUSB0'
ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)

def waitConnection(q):
    while not ser.is_open:
        try:
            ser.open()
            message = f'[SERIAL] connection open {PORT}'
            clue.writeMessageLog(message)
            clue.printConsole(message)

            # throw away queue data
            while not q.empty():
                data = q.get()
                # print(data)

        except serial.SerialException as e:
            pass
        
        time.sleep(1)

def sendMessage(q):
    while True:
        try:
            data = q.get(block=False)
            if ser.is_open:
                ser.write(data.encode('utf-8') + b'\r\n')
                message = f'[SERIAL] transmit alarm data {data}'
                clue.writeMessageLog(message)
                clue.printConsole(message)

        except queue.Empty:
            pass

        except serial.SerialException as e:
            ser.close()
            message = f'[SERIAL] connection lost, {e}'
            clue.writeMessageLog(message)
            clue.printConsole(message)

            waitConnection(q)

        time.sleep(0.1)

# --------------------------
# Management
# --------------------------
def management():
    # management_time = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
    management_send = False

    while True:
        with open("manage.txt", "r", encoding="utf-8") as file:
            text = file.read().strip()

        if not text:
            pass
        else:
            try:
                data = ast.literal_eval(text)
                send_time = datetime.strptime(data.get("timestamp"), "%H:%M:%S").time()
                send_sec = int(send_time.hour * 3600 + send_time.minute * 60 + send_time.second)
                midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

                now = datetime.now()
                now_sec = int((now - midnight).total_seconds())
                
                print(midnight, now_sec, send_sec, management_send)

                if now_sec >= send_sec and not management_send:
                    ser.write(text.encode('utf-8') + b'\r\n')
                    management_send = True

                if now_sec < send_sec:
                    management_send = False

            except (ValueError, SyntaxError):
                pass

        # now = datetime.now()
        # now_sec = int((now - midnight).total_seconds())
        # management_sec = int((management_time - midnight).total_seconds())

        

        time.sleep(60)
# --------------------------
# Main Loop
# --------------------------
if __name__ == "__main__":
    result, data = sql.getAlarmListAll()
    
    if result != 'OK':
        clue.printConsole(f'[ERROR] cannot get data from DB {data}')
        sys.exit(1)

    for alarmlist in data:
        channelList.append(epics.ChannelMonitor(alarmlist['pvname'], q))

    for channelMonitor in channelList:
        channelMonitor.channel.subscribe(channelMonitor.pvname, channelMonitor.alarmMonitor)
        # checkInitState(channelMonitor)
        channelMonitor.channel.startMonitor('field(value)')

    process = multiprocessing.Process(target=sendMessage, args={q})
    process.start()
    # process.join()

    # app.run(host=SERVER_ADDR, port=REST_PORT)
    
    # crate main event loop
    main_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(main_loop)

    # management message send thread
    threading.Thread(target=management, daemon=True).start()

    # flask thread
    threading.Thread(target=run_flask, daemon=True).start()

    # asyncio WebSocket 서버 실행
    main_loop.run_until_complete(ws_server())