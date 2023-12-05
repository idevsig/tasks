# 自动化**任务**

自动化签到、通知、提醒等任务。

## 支持平台

| 类型 | 平台                                     | 多账号 | 支持青龙 | 描述         |
| :--- | :--------------------------------------- | :----- | :------- | :----------- |
| 签到 | [MegStudio](https://studio.brainpp.com/) | 是     | 是       | 免费算力平台 |
| 签到 | [V2EX](https://www.v2ex.com/)            | 是     | 是       | 社交平台     |
| 任务 | 查询域名是否可注册                       | 是     | 是       | 无           |

## 使用

### 1. 设置推送通知环境变量

- **[Bark](https://github.com/finb/bark)**

  ```bash
  export BARK_TOKEN='bark_token'
  ```

- **[Chanify](https://github.com/chanify/chanify)**

  ```bash
  export CHANIFY_TOKEN='chanify_token'
  ```

- **[Lark](https://open.larksuite.com/document/client-docs/bot-v3/add-custom-bot#756b882f)**

  ```bash
  export LARK_TOKEN='lark_token'
  # 若需签名
  export LARK_SECRET='lark_secret'
  ```

- **[飞书](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot#756b882f)**

  ```bash
  export FEISHU_TOKEN='feishu_token'
  # 若需签名
  export FEISHU_SECRET='feishu_secret'
  ```

- **[PushPlus](http://www.pushplus.plus/push1.html)**

  ```bash
  export PUSHPLUS_TOKEN='pushplus_token'
  ```

### 2. 设置环境变量

- **MegStudio 算力平台**

  ```bash
  # OCR API URL
  # 若 `paddleocr, ddddocr` 依赖无法正常安装，则使用外置的OCR，即该URL必须填写
  export OCR_URL=''

  export MEGSTUDIO_USERNAME='USERNAME1;USERNAME2;USERNAME3'
  export MEGSTUDIO_PASSWORD='PASSWORD1;PASSWORD2;PASSWORD3'
  # or
  export MEGSTUDIO_UID='UID1;UID2;UID3'
  export MEGSTUDIO_TOKEN='TOKEN1;TOKEN2;TOKEN3'
  export MEGSTUDIO_COOKIE='COOKIE1;COOKIE2;COOKIE3'
  ```

- **V2EX**

  ```bash
  export V2EX_COOKIE='your_cookie'
  ```

- **DOMAIN**

  ```bash
  export DOMAIN='example1.com;example2.com;example3.com'
  ```

### 3. 运行

```bash
# 安装依赖
pip install -r requirements.txt

# 执行
python main.py
```

## 支持[青龙面板](https://github.com/whyour/qinglong)

1.  `依赖管理` -> `Python` -> **添加下表的依赖**。  
    \*必需依赖 `requests`
    |服务|依赖|说明|
    |:--|:--|:--|
    |_megstudio_|`ddddocr`,`Pillow==9.5.0`|**非必要**|

    **注意：**  
    1). 自建 **[OCR API 服务](https://github.com/sml2h3/ocr_api_server)** 的相关教程。  
    2). 当环境变量 `OCR_URL` 未设置时，必须安装 `ddddocr` 或 `paddleocr` 依赖（_Docker_ 版可能需要使用 [`debian` 镜像：`whyour/qinglong:debian`](https://github.com/whyour/qinglong#docker)）。

2.  自行选择所需的服务，相关命令查看 **[官方教程](https://github.com/whyour/qinglong#%E5%86%85%E7%BD%AE%E5%91%BD%E4%BB%A4)**。

    ```bash
    ql repo https://github.com/idev-sig/tasks.git "v2ex|megstudio|yuming" "main" "ocr"
    ```

## 技术背景

1. 使用 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 和 [ddddocr](https://github.com/sml2h3/ddddocr) 识别验证码。其中，**PaddleOCR** 识别成功率一般, **ddddocr** 识别成功率更高。支持使用 `ddddocr` 自建 API。

## TODO

1. **&checkmark;** 添加推送通知
2. **&checkmark;** 兼容青龙面板

## 仓库镜像

- https://git.jetsung.com/idev/tasks
- https://framagit.org/idev/tasks
- https://github.com/idev-sig/tasks
