import re
import tempfile
from paddleocr import PaddleOCR
import ddddocr


def ocr_image_paddle(image_path):
    '''
    PaddleOCR ocr image
    https://github.com/PaddlePaddle/PaddleOCR
    :param image_path: 图片地址
    :return: ocr text result
    '''
    try:
        # `ch`, `en`, `fr`, `german`, `korean`, `japan`
        pdocr = PaddleOCR(use_angle_cls=True, show_log=False, lang='en')
        result = pdocr.ocr(image_path, det=False)
        # 提取验证码中的数字
        return ''.join(re.findall(r'\d+', result[0][0][0]))
    except Exception as e:
        print(e)
        return None


def ocr_image_ddddocr(image_path):
    '''
    ddddocr ocr image
    https://github.com/sml2h3/ddddocr
    :param image_path: 图片地址
    :return: ocr text result
    '''
    with open(image_path, 'rb') as file:
        image_bytes = file.read()
    ocr = ddddocr.DdddOcr()
    return ocr.classification(image_bytes)


def temp_image(image_data):
    '''
    保存临时图片
    :param image_data: 图片数据
    :return: 临时文件路径
    '''
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_file.write(image_data)
        return temp_file.name
