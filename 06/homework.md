# 一、使用 Burp 的 Discover Content 功能爬取任意站点的目录，给出爬取过程的说明文档、站点树截图；

## 1. 启动 Burp。
![Alt text](image.png)

## 2. 设置浏览器代理。
![Alt text](image-1.png)

## 3. 访问目标站点。
![Alt text](image-2.png)

## 4. 观察 Burp target 下的 Site Map（站点地图）信息。
![Alt text](image-3.png)

## 5. 使用 Discover Content 功能爬取目标站点的目录。
### 5.1 在 Site Map 中，右键点击目标站点，选择 “Engagement tools--Discover Content”
![Alt text](image-23.png)

### 5.2 Discover Content 说明
![Alt text](image-5.png)
* Control：控制模块，由“发现会话状态”和“排列任务”两部分组成。
* Config：配置，可以配置目标站点（target），文件名（Filenames），文件扩展名（File extensions），发现引擎（Discovery engine）。
* Site map：站点地图

### 5.3 开启爬取
#### 点击 “Session is not running”
![Alt text](image-6.png)
#### 当前url不在 “target scope” 中，这里点击确定，确认执行。
![Alt text](image-7.png)
#### 等待爬取结束
![Alt text](image-8.png)

### 5.4 站点树（Site Map）
![Alt text](image-9.png)

# 二、分别使用 Burp Scan 的主动扫描和被动扫描功能对 DVWA 站点进行扫描，输出扫描报告；
## 1. 被动扫描
### 1.1 被动扫描任务
在启动 Burp Suite 的时候，默认开启，如下图：
![Alt text](image-11.png)
> 说明：   
> Live passive crawl from Proxy (all traffic): 来自于代理的实时被动爬取功能。   
> Live audit from Proxy (all traffic): 来自于代理的实时被动审计功能。
### 1.2 被发现的漏洞列表
![Alt text](image-12.png)
* Issue activity：发现的漏洞列表。
* Advisory: 漏洞的详细描述。
* Request: 发现漏洞的请求信息。
* Response: 发现漏洞的请求响应信息。
### 1.3 设置被动扫描的范围
![Alt text](image-13.png)
分别对 “Live passive crawl from Proxy (all traffic)” 和 “Live audit from Proxy (all traffic)” 中的 URL scope 进行设置。
![Alt text](image-14.png)
### 1.4 查看扫描结果
点击 “Live audit from Proxy (all traffic)” 任务的 “View details” 可以查看被动扫描详情。
![Alt text](image-15.png)

### 1.5 导出扫描报告
![Alt text](image-16.png)
> 在 Dash Board 中的 Issue activity 中选择发现的漏洞，然后右键点击，选择“report selected issues”（导出扫描报告）选项。   
![Alt text](image-17.png)
> 以html格式导出。   
![Alt text](image-18.png)
> 漏洞描述与修复建议描述，漏洞引用等信息，根据需要进行勾选定制。   
![Alt text](image-19.png)
> 漏洞发现时的请求信息设置。   
![Alt text](image-20.png)
> 勾选需要导出的漏洞类型。   
![Alt text](image-21.png)
> 设置导出的目录，以及漏洞的分组形式，可以按照类型分，按照服务器分，按照 URL 分。以及漏洞的级别的过滤设置。   
![Alt text](image-22.png)

# 三、Burp Intruder 爆破题目

> 靶场地址： *****   
> 靶场开放时间：2023.9.9 ~ 2023.9.17   
> 管理员账号 / 密码：******   
> 注意事项：爆破成功的同学请勿修改任何账号的密码，以免影响其他同学正常作业。   

## 1. 老李今年 52 岁了，他最近也在学习网络安全，为了方便练习，他在 DVWA 靶场中增设了一个自己的账号，密码就是他的生日，请你想办法破解出他的账号密码。
## 2. Cookie 老师在 DVWA 靶场中设置了一个账号 Geektime（注意首字母大写），且在靶场中的某处存放了一个文件名为 geekbang.txt 的密码字典，请你想办法找到该字典并尝试爆破，最终获取到账号 Geektime 的正确密码。

# 五、在不依赖于 DVWA 后端数据库的情况，如何通过前端验证的方法判断 DVWA 中的注入点是数字型注入还是字符型注入？（提示：用假设法进行逻辑判断）