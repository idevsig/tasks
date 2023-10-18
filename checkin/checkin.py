#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
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
        this = MegStudio()
        return this.run()

    def v2ex(self):
        '''
        v2ex 签到
        https://www.v2ex.com/
        '''
        this = V2EX()
        return this.run()

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
