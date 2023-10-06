# 自动化签到

## 支持平台

| 平台                                     | 描述         |
| :--------------------------------------- | :----------- |
| [MegStudio](https://studio.brainpp.com/) | 免费算力平台 |

## 使用

```bash
pip install -r requirements.txt

# 设置需签到的平台账号信息
export XXX_TOKEN=XXX

python run.py
```

## 技术背景

1. 使用 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 识别验证码，识别成功率一般般，70% 的成功率。

## TODO

1. 添加推送通知
