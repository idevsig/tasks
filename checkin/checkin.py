

import os
from checkin.megstudio import MegStudio
from checkin.v2ex import V2EX
from notify import Notify


class Checkin:
    def __init__(self) -> None:
        pass

    def megstudio(self):
        '''
        MegStuio MegEngine 免费算力平台签到
        https://studio.brainpp.com/
        '''
        username = os.getenv('MEGSTUDIO_USERNAME', '')
        password = os.getenv('MEGSTUDIO_PASSWORD', '')
        uid = os.getenv('MEGSTUDIO_UID', '')
        token = os.getenv('MEGSTUDIO_TOKEN', '')
        cookie = os.getenv('MEGSTUDIO_COOKIE', '')

        this = MegStudio()
        index = 0
        result = False
        while True:
            if username and password:
                result = this.login(username, password)
            elif uid and token and cookie:
                result = this.checkin(uid, token, cookie)
            else:
                return -1
            if result or index >= 5:
                break
            if not result:
                index = index + 1

        if result:
            print('megstudio checkin success')
            return 1
        else:
            print('megstudio checkin failed')

    def v2ex(self):
        '''
        v2ex 签到
        https://www.v2ex.com/
        '''
        cookie = os.getenv('V2EX_COOKIE', '')

        this = V2EX()
        if cookie:
            result = this.checkin(cookie)
        else:
            return -1

        if result:
            print('v2ex checkin success')
            return 1
        else:
            print('v2ex checkin failed')

    def run(self):
        done = self.megstudio()
        if done:
            if done == 1:
                Notify('MegStudio CheckIn', 'MegStudio 签到成功', 'daily').send()
        else:
            Notify('MegStudio CheckIn', 'MegStudio 签到失败', 'daily').send()

        done = self.v2ex()
        if done:
            if done == 1:
                Notify('V2EX CheckIn', 'V2EX 签到成功', 'daily').send()
        else:
            Notify('V2EX CheckIn', 'V2EX 签到失败', 'daily').send()
