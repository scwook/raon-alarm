import pymysql

DB_HOST = '192.168.131.194'
# DB_HOST = 'localhost'
DB_USER = 'coma'
DB_PASSWORD = 'coma'
DB_DATABASE = 'coma'

FROM_NUMBER = '0428788831'

connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')

def test(pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:        
            try:
                query='DELETE FROM sms_info WHERE pname=' + "'" + pvName + "'"
                cursor.execute(query)
                conn.commit()

                return 'OK'
            except pymysql.Error as e:
                
                return e

def getDbConnection():
    return connection

# Retrieve all alarm list with sms infomation
def getAlarmListAll():
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

# Retrieve all alarm status
def getAlarmStateAll():
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:        
            query='SELECT * FROM alarm_info'
            cursor.execute(query)
            result = cursor.fetchall()

            return result

# Retrieve only one alarm info for pvName with sms information
def getAlarmListFromPV(pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:        
            query='SELECT * FROM alarm_info WHERE pvname LIKE "%s"' % (pvName)
            cursor.execute(query)
            result = cursor.fetchall()

            for x in result:
                pvname = x['pvname']
                query = 'SELECT * FROM sms_info WHERE pvname="%s"' % (pvname)
                cursor.execute(query)
                x['sms'] = cursor.fetchall()
            
            return result

# Retrieve alarm list related phone
def getAlarmListFromPhone(phone):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:        
            query='SELECT * FROM sms_info WHERE phone LIKE "%s"' % (phone)
            cursor.execute(query)
            result = cursor.fetchall()

            data = []
            for x in result:
                pvname = x['pvname']
                pvAlarmInfo = getAlarmListFromPV(pvname)
                data.append(pvAlarmInfo[0])
            
            return data

# Retrieve sms list for pvName
def getSMSListFromPV(pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:        
            query='SELECT * FROM sms_info WHERE pvname LIKE ' + "'" + pvName + "'"
            cursor.execute(query)
            result = cursor.fetchall()
            
            return result

# Retrieve sms list for phone
def getSMSListFromPhone(phone):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:        
            query='SELECT * FROM sms_info WHERE pvname LIKE ' + "'" + phone + "'"
            cursor.execute(query)
            result = cursor.fetchall()
            
            return result


# Insert new alarm info record
def insertAlarmInfo(data):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            try:
                pvname = data['pvname']
                description = data['description']
                value = data['value']
                operator = data['operator']
                state = data['state']
                activation = data['activation']
                repetation = data['repetation']
                delay = data['dealy']

                query='INSERT INTO alarm_info(pvname, description, value, operator, state, activation, repetation, delay) values("%s", "%s", "%s", "%d", "%s", "%d", "%d", "%d")' % (pvname, description, value, operator, state, activation, repetation, delay)
                cursor.execute(query)

                for x in data['sms']:
                    sms_phone = x
                    sms_pvname = pvname
                    sms_activation = bool(1)
                    sms_query = 'INSERT INTO sms_info(phone, pvname, activation) values("%s", "%s", "%d")' %(sms_phone, sms_pvname, sms_activation)
                    cursor.execute(sms_query)

                conn.commit()
                return 'OK'
            
            except pymysql.err as e:
                
                return e

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

            return 'OK'


def deleteAlarmInfo(pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:        
            try:
                query='DELETE FROM sms_info WHERE pvname=' + "'" + pvName + "'"
                cursor.execute(query)
                conn.commit()

                query='DELETE FROM alarm_info WHERE pvname=' + "'" + pvName + "'"
                cursor.execute(query)
                conn.commit()

                return 'OK'
            except pymysql.err as e:
                
                return e

# def updateAlarmRecord(data):
#     with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:

#         with conn.cursor() as cursor:        
#             query = 'UPDATE alarm_info SET description="%s", value="%s", operator=%d, state="%s", activation=%d, repetation=%d, delay=%d WHERE pvname="%s"' % (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[0])
#             cursor.execute(query)
#             conn.commit()

def updateAlarmFieldStr(pvName, field, strValue):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            try:  
                query = 'UPDATE alarm_info SET %s="%s" WHERE pvname="%s"' % (field, strValue, pvName)
                cursor.execute(query)
                conn.commit()
                return 'OK'
            
            except pymysql.err as e:

                return e
            
def clearAlarm():
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:        
            query = 'UPDATE alarm_info SET state="normal"'
            cursor.execute(query)
            conn.commit()

def updateAlarmInfo(data):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            try:
                pvname = data['pvname']
                description = data['description']
                value = data['value']
                operator = data['operator']
                repetation = data['repetation']
                delay = data['dealy']

                query = 'UPDATE alarm_info SET description="%s", value="%s", operator="%d", repetation="%d", delay="%d" WHERE pvname="%s"' % (description, value, operator, repetation, delay, pvname)
                cursor.execute(query)

                delete_query = 'DELETE FROM sms_info WHERE pvname="%s"' % (pvname)
                cursor.execute(delete_query)

                for x in data['sms']:
                    sms_phone = x
                    sms_pvname = pvname
                    sms_activation = bool(1)
                    sms_query = 'INSERT into sms_info(phone, pvname, activation) values("%s", "%s", "%d")' %(sms_phone, sms_pvname, sms_activation)
                    cursor.execute(sms_query)

                conn.commit()
                return 'OK'
            
            except pymysql.err as e:
                
                return e

def updateAlarmFieldInt(pvName, field, intValue):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            try:            
                query = 'UPDATE alarm_info SET %s="%d" WHERE pvname="%s"' % (field, intValue, pvName)
                cursor.execute(query)
                conn.commit()
                return 'OK'
            
            except pymysql.err as e:
                
                return e

def updateSMSFieldInt(phone, pvName, field, value):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            try:
                query='UPDATE sms_info SET %s="%d" WHERE phone="%s" AND pvname="%s"' % (field, value, phone, pvName)
                cursor.execute(query)
                conn.commit()
                return 'OK'
            
            except pymysql.err as e:
                
                return e

def deleteSMSListFromPhone(phone):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            try:
                query='DELETE FROM sms_info WHERE phone=' + "'" + phone + "'"
                cursor.execute(query)
                conn.commit()

                return 'OK'
            
            except pymysql.err as e:
                return e

def deleteSMSListFromPVName(pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            try:
                query='DELETE FROM sms_info WHERE pvname=' + "'" + pvName + "'"
                cursor.execute(query)
                conn.commit()

            except pymysql.err as e:
                return e

def deleteSMSList(phone, pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            try:
                query='DELETE FROM sms_info WHERE phone=' + "'" + phone + "'" + ' AND pvname=' + "'" + pvName + "'"
                cursor.execute(query)
                conn.commit()

                return 'OK'

            except pymysql.err as e:
                return e

def insertSMSInfo(phone, pvName):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8') as conn:
        with conn.cursor() as cursor:
            try:
                query='INSERT INTO sms_info(phone, pvname) values("%s", "%s")' % (phone, pvName)
                cursor.execute(query)
                conn.commit()

                return 'OK'
            
            except pymysql.err as e:
                return e