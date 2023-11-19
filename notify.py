import base64
import hashlib
import hmac
import os
import json
import time
import requests
import threading


class Notify:
    """
    Notify class for sending notifications using Bark API.
    """

    def __init__(self, title, message, group=None, copy=None):
        """
        Constructor for Notify class.

        Args:
            title (str): The title of the notification.
            message (str): The message content of the notification.
            group (str): The group to which the notification belongs.
            copy (str): The copy content of the notification.
        """
        self.title = title
        self.message = message
        self.group = group
        self.copy = copy

        self.json_type = 'application/json; charset=utf-8'

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
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def bark(self):
        """
        Send a notification using Bark API.
        https://github.com/finb/bark
        """
        # Check if BARK_TOKEN is set
        token = os.getenv('BARK_TOKEN')
        # print(token)
        if not token:
            return

        headers = {'Content-Type': self.json_type}
        url = 'https://api.day.app/push'
        data = {
            "body": self.message,
            "title": self.title,
            # "group": self.group,
            # "copy": self.copy,
            "device_key": token,
        }

        try:
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

        headers = {'Content-Type': self.json_type}
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

        headers = {'Content-Type': self.json_type}
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

    def send(self):
        bark = threading.Thread(target=self.bark)
        chanify = threading.Thread(target=self.chanify)
        lark = threading.Thread(target=self.lark)
        feishu = threading.Thread(target=self.feishu)
        
        bark.start()
        chanify.start()
        lark.start()
        feishu.start()
    
        bark.join()
        chanify.join()
        lark.join()
        feishu.join()


# 使用示例
if __name__ == "__main__":
    notifier = Notify("Test Title", "Test Notify Server", "test", "复制")
    notifier.bark()
    notifier.chanify()
    notifier.lark()
    notifier.feishu()