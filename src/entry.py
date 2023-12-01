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

    except Exception as e:
        print(e)


def entry():
    v2ex = threading.Thread(target=task, args=(V2EX().run, 'V2EX'))
    megstudio = threading.Thread(target=task, args=(MegStudio().run, 'MegStudio'))

    v2ex.start()
    megstudio.start()

    v2ex.join()
    megstudio.join()
