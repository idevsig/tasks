#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Skiy Chan'

import os
from pkg.notifier.dingtalk import Dingtalk
from pkg.notifier.serverchan import Serverchan
from pkg.provider.smzdm import Smzdm
from pkg.provider.v2ex import V2ex

"""
签到：SMZDM、V2EX
"""

class Check(object):

    def __init__(self):
        self.config = {
            'notify': {
                'dingtalk': False,
                'serverchan': False,
            }
        }

        self.config['notify'] = self.get_notifier()

        print(self.config)

    '''
    Notifier
    '''
    def get_notifier(self):
        dingtalk = False
        serverchan = False

        DINGTALK_ROBOT_TOKEN = os.environ.get('DINGTALK_ROBOT_TOKEN')
        DINGTALK_ROBOT_SECRET = os.environ.get('DINGTALK_ROBOT_SECRET')
        SERVERCHAN_SENDKEY = os.environ.get('SERVERCHAN_SENDKEY')

        if (isinstance(DINGTALK_ROBOT_TOKEN,str) and len(DINGTALK_ROBOT_TOKEN)>0) and (isinstance(DINGTALK_ROBOT_SECRET,str) and len(DINGTALK_ROBOT_SECRET)>0):
            dingtalk = True

        if isinstance(SERVERCHAN_SENDKEY,str) and len(SERVERCHAN_SENDKEY)>0:
            serverchan = True

        self.notifier_dingtalk = Dingtalk(token=DINGTALK_ROBOT_TOKEN, secret=DINGTALK_ROBOT_SECRET)
        self.notifier_serverchan = Serverchan(token=SERVERCHAN_SENDKEY)

        return {
            'dingtalk': dingtalk, 
            'serverchan': serverchan
            }

    '''
    SMZDM SIGN
    '''
    def smzdm_sign(self):
        cookie = os.environ.get('SMZDM_COOKIE')

        if cookie:
            print('smzdm_sign')
            self.notifier(msg = Smzdm(cookie).check_in(), title='「什么值得买」签到')

        else:
            print('no smzdm cookie')

    '''
    V2EX SIGN
    '''
    def v2ex_sign(self):
        cookie = os.environ.get('V2EX_COOKIE')

        if cookie:
            print('v2ex_sign')
            self.notifier(msg = V2ex(cookie).check_in(), title='「V2EX」签到')

        else:
            print('no v2ex cookie')

    def notifier(self, msg, title):
        print(msg)
        if self.config['notify']['dingtalk']:
            self.notifier_dingtalk.push(msg)

        if self.config['notify']['serverchan']:
            self.notifier_serverchan.push(msg=msg, title=title)

if __name__ == '__main__':
    c = Check()

    func = ['smzdm_sign', 'v2ex_sign']
    
    for n in func:
        if n == 'smzdm_sign':
            c.smzdm_sign()
        elif n == 'v2ex_sign':
            c.v2ex_sign()


