import re
import tempfile
import requests


def ocr_image_lib(image_path):
    """
    OCR an image using ddddocr or PaddleOCR library.

    Args:
        image_path (str): The path to the image file to be processed.

    Returns:
        str: The OCR result as a string, or None if OCR fails.
    """
    try:
        import ddddocr
        '''
        ddddocr ocr image
        https://github.com/sml2h3/ddddocr
        '''
        with open(image_path, 'rb') as file:
            image_bytes = file.read()
        ocr = ddddocr.DdddOcr()
        return ocr.classification(image_bytes)
    except ImportError as e:
        print(e)
        pass

    try:
        from paddleocr import PaddleOCR
        '''
        PaddleOCR ocr image
        https://github.com/PaddlePaddle/PaddleOCR
        :param image_path: 图片地址
        :return: ocr text result
        '''
        # `ch`, `en`, `fr`, `german`, `korean`, `japan`
        pdocr = PaddleOCR(use_angle_cls=True, show_log=False, lang='en')
        result = pdocr.ocr(image_path, det=False)
        return ''.join(re.findall(r'\d+', result[0][0][0]))
    except Exception as e:
        print(e)
        return None


def ocr_image_url(url, image_path):
    '''
    ddddocr ocr api image
    https://github.com/sml2h3/ocr_api_server
    :param url: OCR API url
    :param image_path: 图片地址
    :return: ocr text result
    '''
    with open(image_path, 'rb') as file:
        image_bytes = file.read()
    files = {'image': (image_path, image_bytes)}
    resp = requests.post(f"{url}/ocr/file", files=files)
    return resp.text


def temp_image(image_data):
    '''
    保存临时图片
    :param image_data: 图片数据
    :return: 临时文件路径
    '''
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_file.write(image_data)
        return temp_file.name
