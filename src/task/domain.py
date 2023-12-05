#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os
import requests

"""
File: domain.py(检测可注册的域名)
Author: Jetsung
cron: 05 */7 * * *
new Env('检测可注册的域名');
Update: 2023/10/21
"""


class Domain():
    def __init__(self) -> None:
        self.session = requests.Session()

    def task(self, domain):
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.0.0 Safari/537.36 Edg/30.0.1599.101',
            'x-requested-with': 'XMLHttpRequest',
        }

        ispUrl = 'https://www.west.xyz'
        reqUrl = '{}/web/whois/whoisinfo?domain={}&server=&refresh=1'.format(
            ispUrl, domain)

        available = False
        regdate = ""
        expdate = ""
        status = ""

        try:
            response = requests.get(reqUrl, headers=headers)
            if response.status_code != 200:
                raise ValueError(f'status code {response.status_code}')
            resp = response.json()
            if resp['code'] == 200 or resp['code'] == 100:
                available = resp['regdate'] == ''
                status = resp['status']
                if not available:
                    regdate = resp['regdate']
                    expdate = resp['expdate']
            else:
                raise ValueError(f'resp code {resp["code"]}')
        except Exception as e:
            print(f'Error: find domain: {domain}, err:{e}')
            available, regdate, expdate = False, '', ''

        return '{} {}注册，过期时间（{}），状态（{}）'.format(
            domain, '可' if available else '不可', expdate, status), available

    def run(self):
        domain_str = os.getenv('DOMAIN', '')
        message = []

        if domain_str:
            domains = domain_str.split(';')
            for domain in domains:
                msg, available = self.task(domain)
                message.append(f"{msg}\n")

        if not message:
            return None

        return "".join(message)


if __name__ == "__main__":
    message = Domain().run()
    # 兼容青龙面板通知推送
    try:
        from notify import send
        send(f'Find Domain', message)
    except ImportError as e:
        print(e, message)
