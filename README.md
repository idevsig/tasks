# 自动化签到

## 支持平台

| 平台                                     | 是否支持青龙面板                             | 描述         |
| :--------------------------------------- | :------------------------------------------- | :----------- |
| [MegStudio](https://studio.brainpp.com/) | 是 [`megstudio_ql`](checkin/megstudio_ql.py) | 免费算力平台 |
| [V2ex](https://www.v2ex.com/)            | 是                                           | 社交平台     |
| [Fanli](https://www.fanli.com/)          | 是                                           | 购物返利     |

## 使用

### 1. 设置推送通知环境变量

- **Bark**

  ```bash
  export BARK_TOKEN='bark_token'
  ```

- **Chanify**

  ```bash
  export CHANIFY_TOKEN='chanify_token'
  ```

### 2. 设置环境变量

- **MegStudio 算力平台**

  ```bash
  # OCR API URL
  #当青龙面板为 `非 debian` 镜像时，必须填写
  export OCR_URL=''

  export MEGSTUDIO_USERNAME='your_username'
  export MEGSTUDIO_PASSWORD='your_password'
  export MEGSTUDIO_UID='your_uid'
  export MEGSTUDIO_TOKEN='your_token'
  export MEGSTUDIO_COOKIE='your_cookie'
  ```

- **V2EX**

  ```bash
  export V2EX_COOKIE='your_cookie'
  ```

- **Fanli**
  ```bash
  export FANLI_COOKIE='your_cookie'
  ```

### 3. 运行

```bash
# 安装依赖
pip install -r requirements.txt

# 执行
python run.py
```

## 支持[青龙面板](https://github.com/whyour/qinglong)

1.  `依赖管理` -> `Python` -> **添加下表的依赖**。  
    \*必需依赖 `requests`
    |服务|依赖|说明|
    |:--|:--|:--|
    |_megstudio_ql_|`ddddocr`,`Pillow==9.5.0`|**非必要**|

    **注意：**  
    1). 自建 **[OCR API 服务](https://github.com/sml2h3/ocr_api_server)** 的相关教程。  
    2). 当环境变量 `OCR_URL` 未设置时，必须安装 `ddddocr` 依赖（*Docker*版青龙面板时，必须为 [`debian` 版镜像：`whyour/qinglong:debian`](https://github.com/whyour/qinglong#docker)）。

2.  自行选择所需的服务，相关命令查看 **[官方教程](https://github.com/whyour/qinglong#%E5%86%85%E7%BD%AE%E5%91%BD%E4%BB%A4)**。

    ```bash
    ql repo https://jihulab.com/devdo/checkin.git 'v2ex|megstudio_ql' 'run' 'notify|ql' main

    # 海外
    ql repo https://github.com/devdoz/checkin.git 'v2ex|megstudio_ql' 'run' 'notify|ql' main
    ```

## 技术背景

1. 使用 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 和 [ddddocr](https://github.com/sml2h3/ddddocr) 识别验证码。其中，**PaddleOCR** 识别成功率一般, **ddddocr** 识别成功率更高，ddddocr 支持自建 API。

## TODO

1. **&checkmark;** 添加推送通知
2. **&checkmark;** 兼容青龙面板
