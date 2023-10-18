# 自动化签到

## 支持平台

| 平台                                     | 是否支持青龙面板 | 描述         |
| :--------------------------------------- | :--------------- | :----------- |
| [MegStudio](https://studio.brainpp.com/) | 是               | 免费算力平台 |
| [V2ex](https://www.v2ex.com/)            | 是               | 社交平台     |

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

### 4. 运行在[青龙面板](https://github.com/whyour/qinglong)

1. `依赖管理` -> `Python` -> **添加依赖** `requests,ddddocr`

```bash
ql repo https://jihulab.com/devdo/checkin.git "utils|v2ex|megstudio" "run" "notify|ql" main

# 海外
ql repo https://github.com/devdoz/checkin.git "utils|v2ex|megstudio" "run" "notify|ql" main
```

## 技术背景

1. 使用 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 和 [ddddocr](https://github.com/sml2h3/ddddocr) 识别验证码。其中，**PaddleOCR** 识别成功率一般, **ddddocr** 识别成功率更高。

## TODO

1. **&checkmark;** 添加推送通知
2. **&checkmark;** 兼容青龙面板
