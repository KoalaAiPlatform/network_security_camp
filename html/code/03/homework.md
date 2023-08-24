# 一、 在 Docker 中分别以后台方式和交互方式启动 CentOS，对比启动后的容器状态，实现退出容器也能保持其运行状态。

## 1. 查看 CentOS 镜像信息；
```shell
docker images
```
![Alt text](image.png)
## 2. 启动 CentOS；

### 2.1 以后台方式启动 CentOS

```shell
docker run -d centos
```

![Alt text](image-1.png)

#### 查看启动后的容器状态

```shell
docker ps -a
```
![Alt text](image-2.png)

### 2.2 以交互方式启动 CentOS

```shell
docker run -it centos
```
![Alt text](image-3.png)

#### 保持退出
```shell
ctrl + Q + P
```
#### 查看容器状态
![Alt text](image-5.png)

# 二、 在 Docker 中部署 DVWA，要求：DVWA Web 端口映射到 8081，提供访问截图。
![Alt text](image-6.png)

# 三、 MySQL 练习

* 创建一个名为 GeekTime 的数据库；

```shell
 create database GeekTime;
```
![Alt text](image-7.png)

* 在 GeekTime 数据库中创建一张名为 table_Sec 的表，要求有序号、姓名、年龄、性别字段；
```mysql

create table table_Sec (
    id int unsigned auto_increment,
    name varchar(32) null,
    age int unsigned default 0,
    sex varchar(10) default 'man',
    primary key (id)
);
```

![Alt text](image-8.png)
* 在 table_Sec 表中插入数据，序号是 20230819，姓名是拼音缩写，年龄、性别无要求 ;

```mysql
insert into table_Sec values (20230819,'zs',18,'man');
```
![Alt text](image-9.png)

* 使用 Navicat 连接你所创建的数据库，查看个人信息并提供截图。

![Alt text](image-10.png)

# 四、 回顾课件中关于 HTTP 协议的相关知识点，包括格式、请求方法、状态码等，练习使用 HackBar 工具。