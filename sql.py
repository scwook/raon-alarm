import pymysql

# DB_HOST = '192.168.131.162'
DB_HOST = 'localhost'
DB_USER = 'scwook'
DB_PASSWORD = 'qwer1234'
DB_DATABASE = 'alarm_sms'

FROM_NUMBER = '0428788831'

def getSMSList(pvName):

    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    # searchPV = 'scwook:ai1'
    query='SELECT * FROM sms_info WHERE pvname LIKE ' + "'" + pvName + "'"

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    return result
    # smsList = []
    # for x in alarmSMS:
    #     toNumber = x[0]
    #     smsMessage = 'test message'

    #     smsList.append({'to':toNumber, 'from':FROM_NUMBER, 'text': smsMessage})
        
    # return smsList


def getAlarmInfo(pvName):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    query='SELECT * FROM alarm_info WHERE pvname LIKE ' + "'" + pvName + "'"

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchone()

    conn.close()

    return result

def getEntireAlarmList():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    query='SELECT * FROM alarm_info'

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    return result

def getAlarmLog(pvName):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    query='SELECT * FROM alarm_log WHERE pvname LIKE ' + "'" + pvName + "'"    

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    return result

def setAlarmLog():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    query='INSERT INTO alarm_log(date, pvname, log) values()'
    print('aa')

    insertSnapshotQuery = 'INSERT INTO snapshot_info(timestamp,description,eventid) values(' + snapshotTimestamp + "," + snapshotDescription + "," + lastEventIDStr + ")"
    timeleap.execute(insertSnapshotQuery)
    conn.commit()

def deleteAlarmInfo(pvName):
    print('aa')

def updateAlarmInfo(pvName):
    print('aa')

def deleteSMSList(phone, pvName):
    print('aa')

def setSMSList(phone, pvName):
    print('aa')



r = getSMSList('scwook:ai1')
print(r)

    # smsData = {'messages': smsList}
    # print(smsData)
# data = {
#     'messages': [
#         {
#             'to': '01048792718',
#             'from': '01048792718',
#             'text': 'Message Test Value: 1.2E-9Torr'
#         }
#         # ...
#         # 1만건까지 추가 가능
#     ]
# }