# /usr/bin/env python3
# _*_ coding:utf-8 _*_
import os
import re
import requests

"""
File: v2ex.py(V2ex签到)
Author: Jetsung
cron: 40 */10 * * *
new Env('V2ex签到');
Update: 2023/12/01
"""


class V2EX():
    '''
    V2EX
    https://www.v2ex.com/
    '''

    def __init__(self) -> None:
        self.session = requests.Session()
        self.daily_url = 'https://v2ex.com/mission/daily'

    def headers(self, cookie):
        userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
        v2exDomain = "https://www.v2ex.com"
        headers = {
            "User-Agent": userAgent,
            "Referer": v2exDomain,
            "Cookie": cookie,
        }
        self.session.headers.update(headers)

    def once(self):
        response = self.session.get(self.daily_url, timeout=120)
        # print(response.text)
        if '需要先登录' in response.text:
            return [-1, 'Cookie 已失效']
        elif '每日登录奖励已领取' in response.text:
            return [0, '已经签到过']
        return [1, re.compile(r'once\=\d+').search(response.text)]

    def checkin(self, cookie=None):
        if not cookie:
            return None

        try:
            self.headers(cookie)
            state, once = self.once()
            if state == -1:
                return False
            if state == 0:
                return True

            # 签到
            checkin_api = "{}/redeem?{}".format(self.daily_url, once[0])
            response = self.session.get(
                checkin_api, timeout=120)
            # print(response.text)

            # 签到结果
            response = self.session.get(self.daily_url, timeout=120)
            # print(response.text)
            if '每日登录奖励已领取' in response.text:
                return True
            elif '登录' in response.text:
                print('未登录')
        except Exception as e:
            print('checkin failed: {}'.format(e))
        return False

    def run(self):
        cookie = os.getenv('V2EX_COOKIE', '')
        if not cookie:
            return None

        checked = self.checkin(cookie)
        if checked:
            print('v2ex checkin success')
        else:
            print('v2ex checkin failed')
        text = '成功' if checked else '失败'
        return f"签到{text} \n"
        # return checked


if __name__ == "__main__":
    message = V2EX().run()
    # 兼容青龙面板通知推送
    try:
        from notify import send
        send(f'V2EX CheckIn', message)
    except ImportError as e:
        print(e, message)
