# 自动化签到

## 支持平台

| 平台                                     | 描述         |
| :--------------------------------------- | :----------- |
| [MegStudio](https://studio.brainpp.com/) | 免费算力平台 |
| [V2ex](https://www.v2ex.com/)            | 社交平台     |

## 使用

### 1. 设置推送通知环境变量

- **Bark**

```bash
export BARK_TOKEN="bark_token"
```

- **Chanify**

```bash
export CHANIFY_TOKEN="chanify_token"
```

### 2. 设置环境变量

- **MegStudio 算力平台**

```bash
export MEGSTUDIO_USERNAME="your_username"
export MEGSTUDIO_PASSWORD="your_password"
export MEGSTUDIO_UID="your_uid"
export MEGSTUDIO_TOKEN="your_token"
export MEGSTUDIO_COOKIE="your_cookie"
```

- **V2EX**

```bash
export V2EX_COOKIE="your_cookie"
```

### 3. 运行

```bash
# 安装依赖
pip install -r requirements.txt

# 执行
python run.py
```

## 技术背景

1. 使用 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 识别验证码，识别成功率一般。

## TODO

1. **&checkmark;** 添加推送通知
