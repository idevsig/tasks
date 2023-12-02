import base64
import hashlib
import hmac
import os
import json
import time
import requests
import threading

from urllib.parse import quote_plus


class Notify:
    """
    Notify class for sending notifications.
    """

    def __init__(self, message, options={}):
        """
        Constructor for Notify class.

        Args:
            title (str): The title of the notification.
            message (str): The message content of the notification.
            group (str): The group to which the notification belongs.
            copy (str): The copy content of the notification.
        """
        self.message = message
        self.options = options

    def gen_sign(self, timestamp, secret):
        """
        Lark 和 飞书 通知签名
        Generates a sign based on the given timestamp and secret.

        Args:
            timestamp (str): The timestamp to be used in the sign generation.
            secret (str): The secret to be used in the sign generation.

        Returns:
            str: The generated sign.

        """
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        return base64.b64encode(hmac_code).decode('utf-8')

    def get_sign2(self, timestamp, secret):
        """
        钉钉 通知签名
        Generate a URL-safe, base64-encoded HMAC-SHA256 signature.

        Parameters:
            timestamp (str): The timestamp used to generate the signature.
            secret (str): The secret key used in the HMAC-SHA256 algorithm.

        Returns:
            str: The URL-safe, base64-encoded HMAC-SHA256 signature.
        """
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        return quote_plus(base64.b64encode(hmac_code))

    def bark(self):
        """
        Send a notification using Bark API.
        https://github.com/finb/bark
        """
        # Check if BARK_TOKEN is set
        token = os.getenv('BARK_TOKEN')
        if not token:
            return

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = 'https://api.day.app/push'
        data = {
            "body": self.message,
            "device_key": token,
        }

        try:
            if self.options.get('title'):
                data['title'] = self.options.get('title')
            if self.options.get('sound'):
                data['sound'] = self.options.get('sound')
            if self.options.get('group'):
                data['group'] = self.options.get('group')
            if self.options.get('url'):
                data['url'] = self.options.get('url')
            response = requests.post(
                url=url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                print('Bark 推送成功')
            else:
                print('Bark 推送失败')
        except Exception as e:
            print('发送通知时出错:', str(e))

    def chanify(self):
        """
        Send a notification using Chanify API.
        https://github.com/chanify/chanify
        """
        # Check if CHANIFY_TOKEN is set
        token = os.getenv('CHANIFY_TOKEN')
        # print(token)
        if not token:
            return

        url = f'https://api.chanify.net/v1/sender/{token}'
        data = {
            "text": self.message,
        }

        try:
            response = requests.post(
                url=url, data=data)
            if response.status_code == 200:
                print('Chanify 推送成功')
            else:
                print('Chanify 推送失败')
        except Exception as e:
            print('发送通知时出错:', str(e))

    def dingtalk(self):
        """
        Sends a message to DingTalk.

        This function sends a message to DingTalk using the provided DINGTALK_TOKEN. It checks if the token is set, and if not, it returns without sending the message. The message is sent as a POST request to the specified URL, with the content type set to 'application/json; charset=utf-8'. The message content is provided in the 'text' field of the 'content' object in the request data. If the LARK_SECRET is set, a timestamp and sign are added to the request data before sending the message.

        Parameters:
            None

        Returns:
            None
        """
        # Check if DINGTALK_TOKEN is set
        token = os.getenv('DINGTALK_TOKEN')
        # print(token)
        if not token:
            return

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = f'https://oapi.dingtalk.com/robot/send?access_token={token}'
        data = {
            "msgtype": "text",
            "text": {
                "content": self.message
            }
        }

        secret = os.getenv('DINGTALK_SECRET')
        if secret:
            timestamp = str(round(time.time() * 1000))
            sign = self.get_sign2(timestamp, secret)
            url = f'{url}&timestamp={timestamp}&sign={sign}'

        try:
            response = requests.post(
                url=url, headers=headers, data=json.dumps(data), timeout=5)
            respJson = response.json()
            if respJson['errcode'] == 0:
                print('钉钉 推送成功')
            else:
                print('钉钉 推送失败')
        except Exception as e:
            print('发送通知时出错:', str(e))

    def lark(self):
        """
        Send a notification using Lark API.
        https://open.larksuite.com/document/client-docs/bot-v3/add-custom-bot#756b882f
        """
        # Check if LARK_TOKEN is set
        token = os.getenv('LARK_TOKEN')
        # print(token)
        if not token:
            return

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = f'https://open.larksuite.com/open-apis/bot/v2/hook/{token}'
        data = {
            "msg_type": "text",
            "content": {
                "text": self.message
            }
        }

        secret = os.getenv('LARK_SECRET')
        if secret:
            timestamp = str(int(time.time()))
            data["timestamp"] = timestamp
            data["sign"] = self.gen_sign(timestamp, secret)

        try:
            response = requests.post(
                url=url, headers=headers, data=json.dumps(data), timeout=5)
            if response.status_code == 200:
                print('Lark 推送成功')
            else:
                print('Lark 推送失败')
        except Exception as e:
            print('发送通知时出错:', str(e))

    def feishu(self):
        """
        Send a notification using Lark API.
        https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot#756b882f
        """
        # Check if FEISHU_TOKEN is set
        token = os.getenv('FEISHU_TOKEN')
        # print(token)
        if not token:
            return

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = f'https://open.feishu.cn/open-apis/bot/v2/hook/{token}'
        data = {
            "msg_type": "text",
            "content": {
                "text": self.message
            }
        }

        secret = os.getenv('FEISHU_SECRET')
        if secret:
            timestamp = str(int(time.time()))
            data["timestamp"] = timestamp
            data["sign"] = self.gen_sign(timestamp, secret)

        try:
            response = requests.post(
                url=url, headers=headers, data=json.dumps(data), timeout=5)
            if response.status_code == 200:
                print('飞书 推送成功')
            else:
                print('飞书 推送失败')
        except Exception as e:
            print('发送通知时出错:', str(e))

    def pushplus(self):
        """
        http://www.pushplus.plus/push1.html
        """
        # Check if PUSHPLUS_TOKEN is set
        token = os.getenv('PUSHPLUS_TOKEN')
        # print(token)
        if not token:
            return

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = 'https://www.pushplus.plus/send'
        data = {
            "token": token,
            "content": self.message
        }
        if self.options.get('title'):
            data['title'] = self.options.get('title')

        try:
            response = requests.post(
                url=url, headers=headers, data=json.dumps(data), timeout=5)
            if response.status_code == 200:
                print('pushplus 推送成功')
            else:
                print('pushplus 推送失败')
        except Exception as e:
            print('发送通知时出错:', str(e))

    def send(self):
        bark = threading.Thread(target=self.bark)
        chanify = threading.Thread(target=self.chanify)
        dingtalk = threading.Thread(target=self.dingtalk)
        lark = threading.Thread(target=self.lark)
        feishu = threading.Thread(target=self.feishu)
        pushplus = threading.Thread(target=self.pushplus)

        bark.start()
        chanify.start()
        dingtalk.start()
        lark.start()
        feishu.start()
        pushplus.start()

        bark.join()
        chanify.join()
        dingtalk.join()
        lark.join()
        feishu.join()
        pushplus.join()


# 使用示例
if __name__ == "__main__":
    options = {
        "title": "Test Title",
        "sound": "bell.caf",
        "group": "Test Group",
        "url": "https://www.idev.top",
    }
    notifier = Notify("Test Notify Server", options)
    notifier.bark()
    notifier.chanify()
    notifier.dingtalk()
    notifier.lark()
    notifier.feishu()
