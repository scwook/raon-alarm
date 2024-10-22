import time
import sql
import epics
import json
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

# SERVER_ADDR = 'localhost'
# SERVER_ADDR = '192.168.131.161'
SERVER_ADDR = '192.168.150.219'


app = Flask(__name__)
CORS(app)

# conn = sql.getDbConnection()
alarmList = sql.getAlarmList()
channelList = list()
monitoringList = list()

for x in alarmList:
    channelList.append(epics.ChannelMonitor(x))

for y in channelList:
    y.channel.subscribe(y.alarmInfo['pvname'], y.alarmMonitor)
    y.channel.startMonitor('field(value)')

# channelList[0].channel.startMonitor()

# channelList[0].channel.subscribe(channelList[0].alarmInfo['pvname'], channelList[0].alarmMonitor)
# channelList[1].channel.subscribe(channelList[1].alarmInfo['pvname'], channelList[1].alarmMonitor)

# channelList[0].channel.startMonitor()
# time.sleep(10)

# pv = 'scwook:ai1'

# for x in alarmList:
#     if x['pvname'] == pv:
#         x['activation'] = False
#         print('%s activation False' % (x['pvname']))

def restartMonitoring(pvname):
    for y in channelList:
        print(y.alarmInfo['pvname'], pvname)
        if y.alarmInfo['pvname'] == pvname:
            y.channel.stopMonitor()
            time.sleep(1)
            y.channel.startMonitor('field(value)')

@app.route('/', methods=['POST'])
def test():
    formData = request.form
    print(formData)
    return "OK"

@app.route('/updateAlarmInfo', methods=['POST'])
def updateAlarmInfo():
    jsonData = request.get_json()
    pvname = jsonData['pvname']
    description = ""
    value = jsonData['value']
    operator = int(jsonData['condition'])
    delay = int(jsonData['delay'])
    repetation = int(jsonData['repetation']) * 60
    sms = jsonData['phone']

    recordData = {'pvname':pvname, 'description':description, 'value':value, 'operator':operator, 'dealy':delay, 'repetation':repetation, 'sms':sms}

    sql.updateAlarmInfo(recordData)
    return 'OK'

@app.route('/insertAlarmInfo', methods=['POST'])
def insertAlarmInfo():
    jsonData = request.get_json()
    pvname = jsonData['pvname'].strip()
    description = ""
    value = jsonData['value']
    operator = int(jsonData['condition'])
    state = 'normal'
    activation = bool(1)
    delay = int(jsonData['delay'])
    repetation = int(jsonData['repetation']) * 60
    sms = jsonData['phone']

    recordData = {'pvname':pvname, 'description':description, 'value':value, 'operator':operator, 'state': state, 'activation': activation, 'dealy':delay, 'repetation':repetation, 'sms':sms}
    # print(recordData)

    sql.insertAlarmInfo(recordData)
    return 'OK'

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
        sql.updateAlarmFieldStr(pvname, field, value)

    elif field == 'description' or field == 'value':
        sql.updateAlarmFieldStr(pvname, field, value)

    elif field == 'state':
        sql.updateAlarmFieldStr(pvname, field, value)
        restartMonitoring(pvname)

    elif field == 'operator' or field == 'repetation' or field == 'delay':
        value = int(value)
        sql.updateAlarmFieldInt(pvname, field, value)

    elif field == 'activation':
        value = bool(value)
        sql.updateAlarmFieldInt(pvname, field, value)
        
    else:
        return 'Field name error'

    return 'OK'

@app.route('/smsInfoUpdate', methods=['POST'])
def setSMSInfoUpdate():
    jsonData = request.get_json()
    phone = jsonData['phone']
    pvname = jsonData['pvname']
    field = jsonData['field']
    value = jsonData['value']

    sql.updateSMSFieldInt(phone, pvname, field, value)

    return 'OK'

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

@app.route('/deleteAlarmInfo/<pvname>', methods=['GET'])
def deleteAlarmInfo(pvname):
    sql.deleteAlarmInfo(pvname)

    return 'OK'

@app.route('/deleteSMSInfo', methods=['POST'])
def deleteSMSInfo():
    jsonData = request.get_json()
    phone = jsonData['phone']
    pvname = jsonData['pvname']
    sql.deleteSMSList(phone, pvname)

    return 'OK'

if __name__ == "__main__":
    app.run(host=SERVER_ADDR, port="8000")