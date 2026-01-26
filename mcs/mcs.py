import pymysql
import datetime

DB_HOST = '10.1.2.76'
DB_USER = 'raon'
DB_PASSWORD = 'raon2018!'
DB_DATABASE = 'mysql'

FROM_NUMBER = '0428788933'

def sendMMS(user, message):
    with pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE) as conn:
        with conn.cursor() as cursor:
            try:
                dest_info = 'COMA^' + user
                # query = "INSERT INTO sdk_sms_send(USER_ID,SCHEDULE_TYPE,SUBJECT,SMS_MSG,CALLBACK_URL,NOW_DATE,SEND_DATE,CALLBACK,DEST_TYPE,DEST_COUNT,DEST_INFO) values('raon',0,'','TEST SCWOOK','',DATE_FORMAT(NOW(),'%Y%m%d%H%i%s'),DATE_FORMAT(NOW(),'%Y%m%d%H%i%s'),'0428788880',0,1,'EMS^01094402718')"
                query = f'INSERT INTO sdk_mms_send(USER_ID,SCHEDULE_TYPE,SUBJECT,NOW_DATE,SEND_DATE,CALLBACK,DEST_COUNT,DEST_INFO,MSG_TYPE,MMS_MSG,CONTENT_COUNT,CONTENT_DATA) values("raon",0,"Control Message Alarm",DATE_FORMAT(NOW(),"%Y%m%d%H%i%s"),DATE_FORMAT(NOW(),"%Y%m%d%H%i%s"),"0428788831",1,"{dest_info}",0,"{message}",0,"")'
                cursor.execute(query)

                conn.commit()

                return True
            except pymysql.err as e:
                # print(e)
                return e


def test(user, message):
    dest_info = 'COMA^' + user
    query = f'INSERT INTO sdk_mms_send(USER_ID,SCHEDULE_TYPE,SUBJECT,NOW_DATE,SEND_DATE,CALLBACK,DEST_COUNT,DEST_INFO,MSG_TYPE,MMS_MSG,CONTENT_COUNT,CONTENT_DATA) values("raon",0,"Control Message Alarm",DATE_FORMAT(NOW(),"%Y%m%d%H%i%s"),DATE_FORMAT(NOW(),"%Y%m%d%H%i%s"),"0428788831",1,"{dest_info}",0,"{message}",0,"")'
    # print(datetime.datetime.now(), message)

    return True