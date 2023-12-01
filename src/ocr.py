#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import requests


class OCR():
    def __init__(self):
        self.ocr_api_url = None
        self.image_path = None
        self.image_data = None
        self.image_url = None

    def set_ocr_api_url(self, url):
        self.ocr_api_url = url

    def set_image_path(self, path):
        self.image_path = path

    def set_image_data(self, data):
        self.image_data = data

    def set_image_url(self, url):
        self.image_url = url

    def extract(self):
        try:
            # image data
            if self.image_url:
                img_res = requests.get(self.image_url)
                self.image_data = img_res.content
            elif self.image_path:
                with open(self.image_path, 'rb') as f:
                    self.image_data = f.read()

            # get code
            if self.ocr_api_url:
                return self.from_url()

            code = self.from_dep_ddddocr()
            if code is None:
                return self.from_dep_paddleocr()
            return code
        except Exception as e:
            print(e)

    def from_url(self):
        '''
        ddddocr ocr api
        https://github.com/sml2h3/ocr_api_server
        '''
        files = {'image': ('image.png', self.image_data)}
        resp = requests.post(f"{self.ocr_api_url}/ocr/file", files=files)
        print('using ddddocr ocr url')
        return resp.text

    def from_dep_ddddocr(self):
        try:
            import ddddocr
            '''
            ddddocr ocr image
            https://github.com/sml2h3/ddddocr
            '''
            ocr = ddddocr.DdddOcr()
            print('using ddddocr')
            return ocr.classification(self.image_data)
        except ImportError as e:
            print(e)
            return None

    def from_dep_paddleocr(self):
        try:
            from paddleocr import PaddleOCR
            '''
            PaddleOCR ocr image
            https://github.com/PaddlePaddle/PaddleOCR
            '''
            # `ch`, `en`, `fr`, `german`, `korean`, `japan`
            pdocr = PaddleOCR(use_angle_cls=True, show_log=False, lang='en')
            result = pdocr.ocr(self.image_data, det=False)
            print('using paddleocr')
            return ''.join(re.findall(r'\d+', result[0][0][0]))
        except Exception as e:
            print(e)
            return None
