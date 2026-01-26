import requests
import sql

url = "http://192.168.131.23:17665/mgmt/bpl/getAllPVs"
response = requests.get(url)

# HTTP 상태 코드 확인
response.raise_for_status()

# JSON → 파이썬 객체로 변환
data = response.json()

for pv in data:
    recordData = {'pvname': pv, 'description': '', 'value': '0', 'operator':0, 'state':'normal', 'activation':0, 'dealy':5, 'repetation':0, 'sms':[]}
    sql.insertAlarmInfo(recordData)

# recordData = {'pvname': 'test', 'description': '', 'value': '0', 'operator':0, 'state':'normal', 'activation':0, 'dealy':5, 'repetation':0, 'sms':[]}