import json
import time
import datetime
import uuid
import hmac
import hashlib
import requests
import platform

# 아래 값은 필요시 수정
protocol = 'https'
domain = 'api.coolsms.co.kr'
prefix = ''


def unique_id():
    return str(uuid.uuid1().hex)


def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()


def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()


def get_headers(api_key, api_secret):
    date = get_iso_datetime()
    salt = unique_id()
    combined_string = date + salt

    return {
        'Authorization': 'HMAC-SHA256 ApiKey=' + api_key + ', Date=' + date + ', salt=' + salt + ', signature=' +
                         get_signature(api_secret, combined_string),
        'Content-Type': 'application/json; charset=utf-8'
    }


def get_url(path):
    url = '%s://%s' % (protocol, domain)
    if prefix != '':
        url = url + prefix
    url = url + path
    return url


def send_many(parameter):
    # 반드시 관리 콘솔 내 발급 받으신 API KEY, API SECRET KEY를 입력해주세요
    api_key = 'NCSUL8TG1BRCRWZL'
    api_secret = 'PULOZMTNGYVABEDLKDGVWPO4OVIR9HAC'
    parameter['agent'] = {
        'sdkVersion': 'python/4.2.0',
        'osPlatform': platform.platform() + " | " + platform.python_version()
    }

    return requests.post(get_url('/messages/v4/send-many'), headers=get_headers(api_key, api_secret), json=parameter)


'''
한번 요청으로 1만건의 메시지 발송이 가능합니다.
해당 파일을 통해 별도 import 없이 발송 테스트가 가능합니다.
from 데이터의 경우 반드시 관리 콘솔 내 등록하신 발신번호를 넣으셔야 정상 발송 가능합니다. 
'''
if __name__ == '__main__':
    data = {
        'messages': [
            {
                'to': '01048792718',
                'from': '01048792718',
                'text': 'Message Test Value: 1.2E-9Torr'
            }
            # ...
            # 1만건까지 추가 가능
        ]
    }
    res = send_many(data)
    print(json.dumps(res.json(), indent=2, ensure_ascii=False))
