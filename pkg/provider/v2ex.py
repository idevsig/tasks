'''
V2EX
'''

import requests, re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class V2ex(object):
    def __init__(self, cookie):
        print('v2ex')
        self.session = requests.Session()
        self.set_headers(cookie)
        self.req_url = 'https://v2ex.com/mission/daily'

    def set_headers(self, cookie):
        self.session.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'referer': 'https://v2ex.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.35 Safari/537.36 Edg/96.0.1054.13',
            'cookie': cookie,
        })

    def once(self):
        msg = '「V2EX」 签到'
        # print(self.session.headers)
        r = self.session.get(self.req_url, verify=False, timeout=120)
        # print(r.text)
        if '需要先登录' in r.text:
            msg += "cookie 已失效"
            print("V2EX Cookie 已失效", r.text[:200])
            return [-1, msg]
        elif '每日登录奖励已领取' in r.text:
            msg += ', 今天已经签到过啦！'
            return [0, msg]
        return [1, re.compile(r'once\=\d+').search(r.text)]  

    def check_in(self):
        state, resp = self.once()
        if state == -1 or state == 0:
            return resp
        # print(resp)

        msg = '「V2EX」'
        # 签到
        sign_url = "{}/redeem?{}".format(self.req_url, resp[0])
        sign = self.session.get(sign_url, verify=False, timeout=120)
        # 获取签到情况
        r = self.session.get(self.req_url, verify=False)
        # 获取签到情况
        if '每日登录奖励已领取' in r.text:
            msg += ' 签到成功！'
            # 查看获取到的数量
            check_url = 'https://v2ex.com/balance'
            r = self.session.get(check_url, verify=False, timeout=120)
            data = re.compile(r'\d+?\s的每日登录奖励\s\d+\s铜币').search(r.text)
            msg += data[0] + ''
        elif '登录' in sign.text:
            msg += " cookie 已失效！"
            return msg
        else:
            msg += '签到失败！'

        return msg