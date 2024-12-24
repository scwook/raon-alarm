import pymysql

DB_HOST = '192.168.131.194'
# DB_HOST = 'localhost'
DB_USER = 'coma'
DB_PASSWORD = 'coma'
DB_DATABASE = 'coma'

FROM_NUMBER = '0428788831'

connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')

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
        
re = getAlarmListFromPV('COMA-CTRL:ALARM-MESS:AI1')
if len(re):
    print('1')
else:
    print('0')