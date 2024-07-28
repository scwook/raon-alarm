import pymysql
import json
import datetime
import threading

from pvaccess import *

from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SERVER_ADDR = 'localhost'
DB_HOST = 'localhost'
DB_USER = 'ctrluser'
DB_PASSWORD = 'qwer1234'
DB_DATABASE = 'timeleap'

snapshotRecordDict = dict()
#channelList = list()
connectionMonitorDict = dict()
timerCountDict = dict()

class ChannelMonitor:
    def __init__(self, snapshotid, name):
        self.snapshotid = snapshotid
        self.name = name

    def isConnected(self, status):
        snapshotRecordDict[self.snapshotid][self.name] = status

def disconnectionTimer(snapshotKey):
    timerCountDict[snapshotKey] += 2
    timer = threading.Timer(2, disconnectionTimer, args=[snapshotKey])
    timer.start()

    if timerCountDict[snapshotKey] == 10:
        connectionChannel = connectionMonitorDict[snapshotKey]
        
        for i in range(len(connectionChannel)):
            del connectionChannel[-1]
        
        del connectionMonitorDict[snapshotKey]
        del snapshotRecordDict[snapshotKey]
        del timerCountDict[snapshotKey]

        print("Stop connection monitoring: snapshot %s" %(snapshotKey))

        timer.cancel()

@app.route('/timeleap/snapshot/connection/<snapshotid>', methods=['POST'])
def create_record_connection(snapshotid):
    global connectionMonitorDict
    
    if connectionMonitorDict.get(snapshotid) != None:
        return 'Active'
    
    jsonData = request.get_json()

    channelList = list()
    recordStatusDict = dict()
    index = 0
    for name in jsonData:
        pvname = str(name['pvname'])
        
        recordStatusDict[pvname] = 'false'
        snapshotRecordDict[snapshotid] = recordStatusDict

        channelList.append(Channel(pvname, ProviderType.CA))
        channelList[index].setConnectionCallback(ChannelMonitor(snapshotid, pvname).isConnected)
    
        index += 1

    connectionMonitorDict[snapshotid] = channelList

    timerCountDict[snapshotid] = 0
    disconnectionTimer(snapshotid)

    print("Start connection monitoring: snapshot %s" %(snapshotid))

    return 'OK'

@app.route('/timeleap/retrieve/snapshot/connection/<snapshotid>', methods=['GET'])
def get_record_connection_status(snapshotid):
    timerCountDict[snapshotid] = 0

    if snapshotRecordDict.get(snapshotid) == None:
        return json.dumps({})

    return json.dumps(snapshotRecordDict[snapshotid])

@app.route('/timeleap/snapshot/put', methods=['POST'])
def put_record_data():

    jsonData = request.get_json()

    for name in jsonData:
        putCondition = name['status'] and name['restore']

        if putCondition:
            pvname = str(name['pvname'])
            value = float(name['value'])
           
            channel = Channel(pvname, ProviderType.CA)
            channel.put(value)

    return 'OK'

@app.route('/timeleap/snapshot/get/<snapshotid>', methods=['POST'])
def get_record_data():

    return 'OK'

@app.route('/timeleap/event', methods=['POST'])
def create_event():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    timeleap = conn.cursor()

    jsonData = request.get_json()

    # Insert new event
    dateNow = "'" + str(datetime.date.today()) + "'"
    eventTitle = "'" + jsonData['title'] + "'"

    insertEventQuery = 'INSERT INTO event(date,title) values(' + dateNow + "," + eventTitle + ")"
    timeleap.execute(insertEventQuery)
    conn.commit()

    lastEventQuery = 'SELECT max(eventid) FROM event'
    timeleap.execute(lastEventQuery)
    lastEventID = str(timeleap.fetchone()[0])
    lastEventIDStr = "'" + str(lastEventID) + "'"

    # Insert new snapshot
    snapshotTimestamp = "'" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "'"
    snapshotDescription = "'" + jsonData['description'] + "'"

    insertSnapshotQuery = 'INSERT INTO snapshot_info(timestamp,description,eventid) values(' + snapshotTimestamp + "," + snapshotDescription + "," + lastEventIDStr + ")"
    timeleap.execute(insertSnapshotQuery)
    conn.commit()

    lastSnapshotQuery = 'SELECT max(snapshotid) FROM snapshot_info'

    timeleap.execute(lastSnapshotQuery)
    lastSnapshotID = str(timeleap.fetchone()[0])
    
    # Create new snapshot table
    createTableQuery = 'CREATE TABLE snapshot_' + lastSnapshotID + '(pvname varchar(255) NOT NULL, value varchar(255))'
    timeleap.execute(createTableQuery)
    conn.commit()

    conn.close()

    timeleapDic = {'eventid' : lastEventID, 'snapshotid' : lastSnapshotID}

    return json.dumps(timeleapDic)


@app.route('/timeleap/snapshot', methods=['POST'])
def create_snapshot():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    timeleap = conn.cursor()

    jsonData = request.get_json()

    # Insert new snapshot
    eventID = "'" + jsonData['eventid'] + "'"
    snapshotTimestamp = "'" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "'"
    snapshotDescription = "'" + jsonData['description'] + "'"
    
    insertSnapshotQuery = 'INSERT INTO snapshot_info(timestamp,description,eventid) values(' + snapshotTimestamp + "," + snapshotDescription + "," + eventID + ")"
    timeleap.execute(insertSnapshotQuery)
    conn.commit()
    
    lastSnapshotQuery = 'SELECT max(snapshotid) FROM snapshot_info'

    timeleap.execute(lastSnapshotQuery)
    lastSnapshotID = str(timeleap.fetchone()[0])
    
    # Create new snapshot table
    createTableQuery = 'CREATE TABLE snapshot_' + lastSnapshotID + '(pvname varchar(255) NOT NULL, value varchar(255))'
    timeleap.execute(createTableQuery)
    conn.commit()

    conn.close()

    timeleapDic = {'snapshotid': lastSnapshotID}

    return json.dumps(timeleapDic)

@app.route('/timeleap/retrieve', methods=['GET'])
def get_event_snapshot_list():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    eventCursor = conn.cursor()
    snapshotCursor = conn.cursor()

    eventRetrieveQuery = 'SELECT * FROM event'
    eventCursor.execute(eventRetrieveQuery)

    retrieveArray = []
    for x in eventCursor:
        retrieveDic = {'eventid':x[0], 'date':x[1], 'title':x[2], 'snapshot':[]}

        snapshotRetrieveQuery = 'SELECT * FROM snapshot_info WHERE eventid=' + str(x[0])
        snapshotCursor.execute(snapshotRetrieveQuery)
    
        snapshotArray = []
        for y in snapshotCursor:
            snapshotDic = {'snapshotid':y[0], 'timestamp':y[1], 'description':y[2], 'eventid':y[3]}
            snapshotArray.append(snapshotDic)

        retrieveDic['snapshot'] = snapshotArray
        retrieveArray.append(retrieveDic)

    return json.dumps(retrieveArray, ensure_ascii=False)

@app.route('/timeleap/retrieve/event', methods=['GET'])
def get_event_list():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    timeleap = conn.cursor()

    retrieveQuery = 'SELECT * FROM event'
    timeleap.execute(retrieveQuery)

    eventArray = []
    for x in timeleap:
        eventDic = {'eventid':x[0], 'date':x[1], 'title':x[2]}
        eventArray.append(eventDic)

    return json.dumps(eventArray, ensure_ascii=False)

@app.route('/timeleap/retrieve/snapshot', methods=['GET'])
def get_snapshot_list():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    timeleap = conn.cursor()

    retrieveQuery = 'SELECT * FROM snapshot_info'
    timeleap.execute(retrieveQuery)

    snapshotArray = []
    for x in timeleap:
        snapshotDic = {'snapshotid':x[0], 'timestamp':x[1], 'description':x[2], 'eventid':x[3]}
        snapshotArray.append(snapshotDic)

    return json.dumps(snapshotArray, ensure_ascii=False)
    

@app.route('/timeleap/retrieve/snapshot/record/<id>', methods=['GET'])
def get_record_list(id):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    timeleap = conn.cursor()

    snapshotID = str(id)

    retrieveQuery = 'SELECT * FROM snapshot_' + snapshotID
    timeleap.execute(retrieveQuery)

    recordArray = []
    for x in timeleap:
        recordDic = {'pvname':x[0], 'value':x[1], 'status':'false'}
        recordArray.append(recordDic)

    conn.close()

    return json.dumps(recordArray, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host=SERVER_ADDR, port="9013")
