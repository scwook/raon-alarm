import time
import sql
import epics
import json
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

# SERVER_ADDR = 'localhost'
SERVER_ADDR = '192.168.131.161'

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
    # y.channel.startMonitor()

channelList[0].channel.startMonitor()

# channelList[0].channel.subscribe(channelList[0].alarmInfo['pvname'], channelList[0].alarmMonitor)
# channelList[1].channel.subscribe(channelList[1].alarmInfo['pvname'], channelList[1].alarmMonitor)

# channelList[0].channel.startMonitor()

# time.sleep(10)

# pv = 'scwook:ai1'

# for x in alarmList:
#     if x['pvname'] == pv:
#         x['activation'] = False
#         print('%s activation False' % (x['pvname']))

@app.route('/', methods=['POST'])
def test():
    formData = request.form
    print(formData)
    return "OK"

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

@app.route('/getAlarmData', methods=['GET'])
def getAlarmData():
    result = sql.getAlarmData()

    return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host=SERVER_ADDR, port="8000")