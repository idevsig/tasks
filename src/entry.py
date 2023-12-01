#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import threading

from src.notify import Notify
from src.checkin.v2ex import V2EX
from src.checkin.megstudio import MegStudio


def task(cls, service_name):
    try:
        text = cls()
        if text is None:
            return
        message = "「{}」 \n{}".format(service_name, text)
        Notify(message).send()

        # 青龙面板通知推送
        ql_notify(service_name, message)
    except Exception as e:
        print(e)


def ql_notify(service_name, message):
    # 兼容青龙面板通知推送
    try:
        from notify import send
        send(f'{service_name} CheckIn', message)
    except ImportError as e:
        print("ql notify error: ".format(e))


def entry():
    v2ex = threading.Thread(target=task, args=(V2EX().run, 'V2EX'))
    megstudio = threading.Thread(target=task, args=(MegStudio().run, 'MegStudio'))

    v2ex.start()
    megstudio.start()

    v2ex.join()
    megstudio.join()
