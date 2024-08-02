import pymysql

DB_HOST = '192.168.131.162'
DB_USER = 'scwook'
DB_PASSWORD = 'qwer1234'
DB_DATABASE = 'alarm_sms'

FROM_NUMBER = '0428788831'

conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_DATABASE, charset='utf8')
searchPV = 'scwook:ai1'
query='SELECT * FROM sms_info WHERE pvname LIKE ' + "'" + searchPV + "'"

alarmSMS = conn.cursor()
alarmSMS.execute(query)

smsList = []
for x in alarmSMS:
    toNumber = x[0]
    smsMessage = 'test message'

    smsList.append({'to':toNumber, 'from':FROM_NUMBER, 'text': smsMessage})
    
smsData = {'messages': smsList}
print(smsData)
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