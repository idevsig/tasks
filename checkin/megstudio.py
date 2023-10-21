#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import json
import os
import re
import time
from urllib.parse import parse_qs, urlparse
import requests
import base64
from utils import temp_image, ocr_image_url, ocr_image_lib


class MegStudio():
    '''
    MegStuio MegEngine 免费算力平台
    https://studio.brainpp.com/
    '''

    def __init__(self) -> None:
        self.session = requests.Session()

    def login(self, username, password):
        try:
            # 获取到登录页面
            login_url = 'https://studio.brainpp.com/api/authv1/login?redirectUrl=https://studio.brainpp.com/'
            response = self.session.get(login_url)

            # 取出 login_challenge 值，登录时使用
            parsed_url = urlparse(response.url)
            query_params = parse_qs(parsed_url.query)
            login_challenge_value = query_params.get(
                'login_challenge', [''])[0]

            # 生成验证码请求 URL
            current_time = str(int(time.time() * 1000))
            captcha_url = 'https://account.megvii.com/api/v1/captcha?endpoint=login&_t={}'.format(
                current_time)

            # 请求验证码 URL，获取验证码信息
            response = self.session.get(captcha_url)
            # print(response.content.decode('utf-8'))

            captcha_data = json.loads(response.text)
            if captcha_data['error_code'] != 0:
                raise Exception('get captcha data error')

            # 从验证码结果中获取 biz_id 和 image
            biz_id = captcha_data['data']['biz_id']
            image_base64 = captcha_data['data']['image']
            image_data = base64.b64decode(image_base64)
            # image_buffer = BytesIO(image_data)
            # image = Image.open(image_buffer)
            # image_path = 'output_image.png'
            # image.save(image_path, 'PNG')
            # image.show()
            # image_buffer.close()

            # 保存临时图片
            image_path = temp_image(image_data)

            # OCR API
            ocr_api_url = os.getenv('OCR_URL')
            if ocr_api_url:
                captcha = ocr_image_url(ocr_api_url, image_path)
            else:
                captcha = ocr_image_lib(image_path)
            os.remove(image_path)

            if not captcha:
                return None
            elif captcha == '' or len(captcha) != 4:
                raise Exception('captcha is empty or not 4 digits')

            # 登录
            login_api = 'https://account.megvii.com/api/v1/login'
            headers = {
                'Referer': 'https://studio.brainpp.com/',
                'Content-Type': 'application/json',
            }
            login_data = {
                'username': username,
                'password': password,
                'code': captcha,
                'biz_id': biz_id,
                'login_challenge': login_challenge_value
            }
            response = self.session.post(
                login_api, headers=headers, data=json.dumps(login_data))

            login_data = json.loads(response.text)
            if login_data['error_code'] != 0:
                raise Exception('login failed: {}'.format(
                    login_data['error_msg']))

            if login_data['data']['code'] != 0:
                raise Exception('login error')
            redirect_url = login_data['data']['redirect']
            # allow_redirects 设置为 False，避免重定向请求
            response = self.session.get(
                redirect_url, allow_redirects=False)

            # # 定义一个列表来存储每次跳转的URL和状态码
            # redirect_info = []

            # 处理多级302跳转
            while response.status_code == 302:
                # 获取当前响应的URL
                current_url = response.headers.get('Location', '')

                # 获取当前响应的状态码
                # status_code = response.status_code
                # # 获取当前响应的Set-Cookie值（如果有）
                # set_cookie = response.headers.get('Set-Cookie', '')
                # # 将当前URL和状态码添加到列表中
                # redirect_info.append(
                #     {'url': current_url, 'status_code': status_code, 'set_cookie': set_cookie})

                # 发送下一次跳转请求，继续禁用自动跟踪重定向
                response = self.session.get(current_url, allow_redirects=False)

            # # 输出每次跳转的URL和状态码
            # for info in redirect_info:
            #     print(f'URL: {info["url"]}')
            #     print(f'Status Code: {info["status_code"]}')
            #     print(f'Set-Cookie: {info["set_cookie"]}')

            # 从网页源码中获取 X-CSRF-Token
            csrf_token_match = re.search(
                r'<meta name=X-CSRF-Token content="([^"]+)"', response.text)
            if csrf_token_match:
                csrf_token = csrf_token_match.group(1)
            else:
                raise Exception('X-CSRF-Token not found in the HTML.')

            # 获取用户信息
            userinfo_api = 'https://studio.brainpp.com/api/v1/users/0'
            headers = {
                'X-Csrf-Token': csrf_token,
                # 'Cookie': 'web-session=xxx',
            }
            response = self.session.get(userinfo_api, headers=headers)
            user_data = json.loads(response.text)
            uid = user_data['data']['id']
            # print(uid, csrf_token)

            print('login success')
            return self.checkin(uid=uid, token=csrf_token)
        except Exception as e:
            print('login failed: {}'.format(e))

    def checkin(self, uid, token, cookie=None):
        # X-Csrf-Token
        # Cookie: web-session=xxx
        checkin_api = 'https://studio.brainpp.com/api/v1/users/{}/point-actions/checkin'.format(
            uid)
        headers = {
            'Referer': 'https://studio.brainpp.com/',
            'X-Csrf-Token': token,
        }

        if cookie:
            headers['Cookie'] = cookie

        # print(checkin_api, headers)
        try:
            response = self.session.post(checkin_api, headers=headers)
            print('checkin result: {} {}'.format(
                response.status_code, response.text))

            if response.status_code == 200 or response.status_code == 403:
                return True
        except Exception as e:
            print('checkin failed: {}'.format(e))

    def run(self):
        username = os.getenv('MEGSTUDIO_USERNAME', '')
        password = os.getenv('MEGSTUDIO_PASSWORD', '')
        uid = os.getenv('MEGSTUDIO_UID', '')
        token = os.getenv('MEGSTUDIO_TOKEN', '')
        cookie = os.getenv('MEGSTUDIO_COOKIE', '')

        index = 0
        result = False
        while True:
            if username and password:
                result = self.login(username, password)
            elif uid and token and cookie:
                result = self.checkin(uid, token, cookie)
            else:
                return -1
            if result or result is None or index >= 5:
                break
            if not result:
                index = index + 1

        if result:
            print('megstudio checkin success')
            return 1
        else:
            print('megstudio checkin failed')


if __name__ == "__main__":
    '''
    MegStuio MegEngine 免费算力平台签到
    https://studio.brainpp.com/
    '''
    this = MegStudio()
    this.run()
