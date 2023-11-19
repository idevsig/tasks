#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os
import requests

"""
File: fanli.py(Fanli 签到)
Author: Jetsung
cron: 40 1 * * *
new Env('Fanli 签到');
Update: 2023/11/19
"""


class Fanli():
    '''
    Fanli
    https://www.fanli.com/
    '''

    def __init__(self) -> None:
        self.session = requests.Session()
        self.fanli_url = 'https://huodong.fanli.com/sign82580'

    def headers(self, cookie):
        userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Fanli/7.19.71.6 (ID:1-1069183-65912421924760-17-0; WVC:WK; SCR:1170*2532-3.0)"
        headers = {
            "User-Agent": userAgent,
            "Referer": self.fanli_url,
            "Cookie": cookie,
        }
        self.session.headers.update(headers)

    def checkin(self, cookie=None):
        if not cookie:
            return None

        try:
            self.headers(cookie)

            # 签到
            checkin_api = "{}/ajaxSetUserSign".format(self.fanli_url)
            response = self.session.get(
                checkin_api, timeout=5)
            # print(response.text)

            resp = response.json()
            if resp['status'] == 1:
                return True
        except Exception as e:
            print('checkin failed: {}'.format(e))
        return False

    def run(self):
        '''
        Fanli
        https://www.fanli.com/
        '''
        cookie = os.getenv('FANLI_COOKIE', '')
        checked = False
        if cookie:
            checked = self.checkin(cookie)
        else:
            return None

        if checked:
            print('fanli checkin success')
        else:
            print('fanli checkin failed')
        return checked


if __name__ == "__main__":
    '''
    Fanli 签到
    https://www.fanli.com/
    '''
    this = Fanli()
    done = this.run()

    # 兼容青龙面板通知推送
    try:
        from notify import send
    except ImportError as e:
        print(str(e))
        import sys
        sys.exit()

    if done:
        send('Fanli CheckIn', 'Fanli 签到成功')
    else:
        send('Fanli CheckIn', 'Fanli 签到失败')
