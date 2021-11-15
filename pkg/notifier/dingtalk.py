'''
钉钉通知
'''

import requests

import time
import hmac
import hashlib
import base64
import urllib.parse

class Dingtalk(object):
    def __init__(self, token, secret):
        self.token = token
        self.secret = secret

    def sign(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        # print(timestamp)
        # print(sign)
        return '&timestamp=' + timestamp + '&sign=' + sign

    def push(self, msg):
        print(f'检测到 "钉钉机器人" 准备推送: {msg}')

        sign = self.sign()
        url = 'https://oapi.dingtalk.com/robot/send?access_token={}{}'.format(self.token, sign)

        session = requests.Session()
        session.headers['content-type'] = 'application/json'

        data = '{"msgtype": "text","text": {"content":"' + msg + '"}}'
        response = session.post(url, data=data.encode('utf-8'))
        # print(url)
        # print(response)
        # print(response.json())
        return response