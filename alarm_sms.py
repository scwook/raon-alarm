import time

# from flask import Flask

import sql
import epics


SERVER_ADDR = 'localhost'

# app = Flask(__name__)


conn = sql.getDbConnection()

r = sql.getSMSList(conn, 'scwook:ai1')

print(r)


dbPhone = ['01048792718']

dbSample = [
    {'pvname':'scwook:ai1', 'desc': '', 'value':5.0, 'operator':1, 'state':'normal', 'activation':True, 'lasttime': '0', 'repeat':10, 'delay': 2},
    {'pvname':'scwook:ai2', 'desc': '', 'value':5.0, 'operator':1, 'state':'normal', 'activation':False, 'lasttime': '0', 'repeat':0, 'delay': 2}
    ]

channelList = list()
monitoringList = list()

channelList.append(epics.ChannelMonitor(dbSample[0]))
channelList.append(epics.ChannelMonitor(dbSample[1]))

channelList[0].channel.subscribe(channelList[0].alarmInfo['pvname'], channelList[0].alarmMonitor)
channelList[1].channel.subscribe(channelList[1].alarmInfo['pvname'], channelList[1].alarmMonitor)

channelList[0].channel.startMonitor()

time.sleep(60)
# @app.route('/', methods=['GET'])
# def test():
#     return "OK"

# if __name__ == "__main__":
#     app.run(host=SERVER_ADDR, port="8000")