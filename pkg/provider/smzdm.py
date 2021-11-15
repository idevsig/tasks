'''
SMZDM
'''

import requests

class Smzdm(object):
    def __init__(self, cookies):
        print('smzdm')
        self.session = requests.Session()
        self.set_headers()
        self.session.headers['Cookie'] = cookies.encode('utf-8')    
        self.url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'

    def set_headers(self):
        self.session.headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'zhiyou.smzdm.com',
        'Referer': 'https://www.smzdm.com/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }

    def __json_check(self, msg):
        try:
            res = msg.json()
            # print(res)
            return str(res['error_msg'])
        except Exception as e:
            print(f'Error: {e}')            
            return str(e)

    def check_in(self):
        # print(self.session.headers)
        msg = self.session.get(self.url)
        
        status = '失败'

        resp = self.__json_check(msg)      
        if resp == '':
            status = '成功'
        else:
            status += f', {resp}'

        return f'「什么值得买」每日签到{status}!'