## 自动签到
使用 GitHub Actions 自动签到。

### 支持签到平台
- 什么值得买: https://smzdm.com
- V2EX: https://v2ex.com

### 1. 实现功能
+ 通过 `钉钉群机器人` 推送通知到钉钉群
+ 通过 `SERVERCHAN` 推送简单的运行结果到微信
+ 由 `github actions` 每日早上 1 点定时运行

### 2. 使用方法
1. `Fork` 此项目，欢迎点`star`~
2. 设置签到平台的 cookie 信息    
    2.1. Secret 新增`SMZDM_COOKIE`，从[什么值得买官网](https://www.smzdm.com/) 提取的 cookie 信息。   
    2.2. Secret 新增`V2EX_COOKIE`，从[V2EX 官网](https://v2ex.com/) 提取的 cookie 信息。   
3. （可选）通知   
    3.1. SERVERCHAN 通知：Secret 新增`SERVERCHAN_SENDKEY`，获取方法请[查看文档](https://sct.ftqq.com/)。   
    3.2. 钉钉群机器人通知：Secret 新增`DINGTALK_ROBOT_SECRET` 和 `DINGTALK_ROBOT_TOKEN`，获取方法请查看[「钉钉机器人」](https://developers.dingtalk.com/document/robots/custom-robot-access)。注意，需要[加签](https://developers.dingtalk.com/document/robots/customize-robot-security-settings/title-7fs-kgs-36x)。   
4. `Fork` 后必须修改一下文件，才能执行定时任务, 可修改 `README.md`。


### 3. 其它
#### 3.1 cookie 获取方法
> 以下为例子   
+ 首先使用chrome浏览器，访问[什么值得买官网](https://www.smzdm.com/)， 登陆账号
+ Windows系统可按 `F12` 快捷键打开开发者工具, Mac 快捷键 `option + command + i`
+ 选择开发者工具Network，刷新页面 ,选择第一个`www.smzdm.com`, 找到 `Requests Headers` 里的 `Cookie`。

#### 3.2 更改执行时间
在 `.github/check-in.yml`中
```yml
- cron: '0 0 * * *'
```

> 语法与 Linux 操作系统的 crontab 计划任务相同，具体可百度。因 GitHub Actions 为美西时间，+13 小时为中国时间（即设置的时候需要 -13 小时）。

- 本项目参考了部分“签到”开源项目
  