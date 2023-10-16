import os
import json
import requests


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

    def send(self):
        self.bark()
        self.chanify()


# 使用示例
if __name__ == "__main__":
    notifier = Notify("Test Title", "Test Bark Server", "test", "复制")
    notifier.bark()
    notifier.chanify()
