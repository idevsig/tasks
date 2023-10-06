import tempfile
from paddleocr import PaddleOCR


def ocr_image(image_path):
    '''
    PaddleOCR ocr image
    :param image_path: 图片地址
    :return: ocr result
    '''
    try:
        # `ch`, `en`, `fr`, `german`, `korean`, `japan`
        ocr = PaddleOCR(use_angle_cls=True, show_log=False, lang='en')
        return ocr.ocr(image_path, det=False)

    except Exception as e:
        print(e)
        return None


def temp_image(image_data):
    '''
    保存临时图片
    :param image_data: 图片数据
    :return: 临时文件路径
    '''
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_file.write(image_data)
        return temp_file.name
