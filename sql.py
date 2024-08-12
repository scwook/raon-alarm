import pymysql

DB_HOST = '192.168.131.162'
# DB_HOST = 'localhost'
DB_USER = 'scwook'
DB_PASSWORD = 'qwer1234'
DB_DATABASE = 'alarm_sms'

FROM_NUMBER = '0428788831'

connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')

def getDbConnection():
    return connection

def getAlarmData():
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:        
            query='SELECT * FROM alarm_info'
            cursor.execute(query)
            result = cursor.fetchall()

            for x in result:
                pvname = x['pvname']
                query = 'SELECT * FROM sms_info WHERE pvname="%s"' % (pvname)
                cursor.execute(query)
                x['sms'] = cursor.fetchall()

            return result


def getSMSList(pvName):
    # conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:        
            query='SELECT * FROM sms_info WHERE pvname LIKE ' + "'" + pvName + "'"
            cursor.execute(query)
            result = cursor.fetchall()
            
            return result

def getAlarmInfo(pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:        
            query='SELECT * FROM alarm_info WHERE pvname LIKE ' + "'" + pvName + "'"
            cursor.execute(query)
            result = cursor.fetchone()

            return result

def getAlarmList():
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:        
            query='SELECT * FROM alarm_info'
            cursor.execute(query)
            result = cursor.fetchall()

            return result

def getAlarmLog(pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:        
            query='SELECT * FROM alarm_log WHERE pvname LIKE ' + "'" + pvName + "'"    
            cursor.execute(query)
            result = cursor.fetchall()
            
            return result

def insertAlarmLog(pvname, log):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:        
            query='INSERT INTO alarm_log(pvname, log) values("%s", "%s")' % (pvname, log)
            cursor.execute(query)
            conn.commit()


def deleteAlarmInfo(pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:        
            query='DELETE FROM sms_info WHERE pvname=' + "'" + pvName + "'"
            cursor.execute(query)
            conn.commit()

            query='DELETE FROM alarm_info WHERE pvname=' + "'" + pvName + "'"
            cursor.execute(query)
            conn.commit()

def updateAlarmRecord(data):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:

        with conn.cursor() as cursor:        
            query = 'UPDATE alarm_info SET description="%s", value="%s", operator=%d, state="%s", activation=%d, repetation=%d, delay=%d WHERE pvname="%s"' % (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[0])
            cursor.execute(query)
            conn.commit()

def updateAlarmFieldStr(pvName, field, strValue):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:        
            query = 'UPDATE alarm_info SET %s="%s" WHERE pvname="%s"' % (field, strValue, pvName)
            cursor.execute(query)
            conn.commit()

def clearAlarm():
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:        
            query = 'UPDATE alarm_info SET state="normal"'
            cursor.execute(query)
            conn.commit()

def updateAlarmFieldInt(pvName, field, intValue):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:        
            query = 'UPDATE alarm_info SET %s="%d" WHERE pvname="%s"' % (field, intValue, pvName)
            cursor.execute(query)
            conn.commit()


def deleteSMSListFromPhone(phone):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            query='DELETE FROM sms_info WHERE phone=' + "'" + phone + "'"
            cursor.execute(query)
            conn.commit()

def deleteSMSListFromPVName(pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            query='DELETE FROM sms_info WHERE pvname=' + "'" + pvName + "'"
            cursor.execute(query)
            conn.commit()

def deleteSMSList(phone, pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            query='DELETE FROM sms_info WHERE phone=' + "'" + phone + "'" + ' AND pvname=' + "'" + pvName + "'"
            cursor.execute(query)
            conn.commit()

def insertSMSInfo(phone, pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            query='INSERT INTO sms_info(phone, pvname) values("%s", "%s")' % (phone, pvName)
            cursor.execute(query)
            conn.commit()

    # conn.close()
getAlarmData()

# testData = ('scwook:ai2', 'update', "12.1E-7", 1, 'alarm', 1, 10, 20)
# updateAlarmInfo(testData)

    # smsList = []
    # for x in alarmSMS:
    #     toNumber = x[0]
    #     smsMessage = 'test message'

    #     smsList.append({'to':toNumber, 'from':FROM_NUMBER, 'text': smsMessage})
        
    # return smsList


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