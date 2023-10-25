#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import threading
from checkin.megstudio import MegStudio
from checkin.v2ex import V2EX
from notify import Notify


def checkin(check_in, service_name):
    done = check_in()
    if done is None:
        return

    if done:
        Notify(f'{service_name} CheckIn', f'{service_name} 签到成功', 'daily').send()
    elif done is False:
        Notify(f'{service_name} CheckIn', f'{service_name} 签到失败', 'daily').send()


def main():
    megstudio = threading.Thread(target=checkin, args=(MegStudio().run, 'MegStudio'))
    v2ex = threading.Thread(target=checkin, args=(V2EX().run, 'V2EX'))

    megstudio.start()
    v2ex.start()

    megstudio.join()
    v2ex.join()


if __name__ == "__main__":
    main()
