# 一、分别使用 AWVS 和 Xray（被动扫描模式）去扫描任一 SRC 允许测试的目标，对比扫描结果的不同；

## 1. AWVS

### 1.1 AWVS 的安装与启动

#### 搜索

```shell
docker search awvs
```

#### 获取镜像

```shell
docker pull dockermi3aka/awvs
```

#### 启动

```shell
docker run -dit -p 3443:3443 dockermi3aka/awvs
```

#### 访问

```url
https://huanxue.com:3443/#/dashboard
```

![Alt text](image.png)

### 1.2 AWVS 扫描（应用类主动扫描）

#### 1.2.1 添加目标站点，位置：“Targets--Add Targets”，输入后点击 “save” 进行保存。

![Alt text](image-5.png)

#### 1.2.2 选择 “scan”

![Alt text](image-1.png)

##### 点击新建扫描任务按钮 “New Scan”

![Alt text](image-2.png)

##### 勾选目标站点，点击 “scan”

![Alt text](image-6.png)

##### 扫描结果

![Alt text](image-11.png)

## 2. Xray

### 2.1 Xray 的安装

#### 2.1.1 访问 Xray 官网

```url
https://docs.xray.cool
```
#### 2.1.2 查看文档页中的快速开始

```url
https://docs.xray.cool/#/tutorial/prepare
```

#### 2.1.3 下载

##### 下载地址

```url
https://stack.chaitin.com/tool/detail/1
```

##### 下载 mac 版本的

![Alt text](image-8.png)

#### 2.1.4 压缩包解压到指定目录

![Alt text](image-12.png)

#### 2.1.5 启动前，修改配置

![Alt text](image-13.png)

#### 2.1.6 启用xray被动模式代理

```shell
./xray_darwin_amd64 webscan --listen 127.0.0.1:7777 --html-output test.html
```

![Alt text](image-14.png)

#### 2.1.7 启用浏览器代理

![Alt text](image-15.png)

#### 2.1.8 访问测试站点页面，进行简单的功能测试

![Alt text](image-16.png)

#### 2.1.9 查看生成的报告

![Alt text](image-17.png)

## 3. 扫描结果对比

|对比项|项目|描述|
|---|---|---|
|扫描方式|AWVS|主动扫描|
| |Xray|被动扫描|
|查看方式|AWVS|直接通过可视化系统，访问 Scans 页面，点击对应的条目，就可查看扫描结果|
| |Xray|通过命令行中的 --html-output 选项来指定结果的输出类型，名称与位置|
|站点安全现状描述|AWVS|扫描结果中可以看到目标站点当前的整体风险等级评价|
| |Xray|无|
|系统信息|AWVS|扫描结果中有目标站点的系统信息描述|
| |Xray|无|
|漏洞描述|AWVS|漏洞信息描述详细，有具体的漏洞等级，发现漏洞时的请求和响应，修复建议以及漏洞编号信息|
| |Xray|漏洞信息描述简明，仅有有发现漏洞的插件，以及漏洞类型，发现漏洞时的请求和响应|

**个人总结：** AWVS 的扫描结果比较详细，内容丰富，但其因主动扫描的方式，很可能会被安全防护设备拦截，所以通常会用于内网项目的扫描，操作时最好和运维团队打招呼。Xray 的扫描结果言简意赅，没有漏洞等级以及漏洞编号等描述，适合有一定安全从业经验和了解常见漏洞及其原理的安全工作者使用。

# 二、使用 Nessus 扫描任一主机，要求使用全端口扫描，提供主机扫描报告；
# 三、安装 Burp，分别在本机上实现全局代理和局部代理，提供设置过程的说明文档；
# 四、利用 Burp 实现对 HTTPS 站点的抓包。
