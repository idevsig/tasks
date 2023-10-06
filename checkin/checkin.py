

import os
from checkin.megstudio import MegStudio


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
        if username and password:
            result = this.login(username, password)
        elif uid and token and cookie:
            result = this.checkin(uid, token, cookie)
        else:
            return

        if result:
            print('megstudio checkin success')
        else:
            print('megstudio checkin failed')

    def run(self):
        self.megstudio()
