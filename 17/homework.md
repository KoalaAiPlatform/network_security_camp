# 一、通过前端表单提交请求到后端 PHP 代码处理，请求内容为年龄 + 姓名，使用 GET 和 POST 请求，前端展示做 xss 漏洞防御。
## 1. [制作一个前端的表单提交](./user.html)
![Alt text](image.png)
## 2. [写一个用于接收请求的php](./userInfo.php)
![Alt text](image-1.png)
## 3. 启动服务
![Alt text](image-2.png)
## 4. 提交数据
![Alt text](image-3.png)
## 5. XSS攻击
![Alt text](image-4.png)   
![Alt text](image-5.png)   
## 6. 防御XSS
使用 `htmlspecialchars` 函数，改造之前的php源码。   
![Alt text](image-7.png)
## 7. 再次提交
![Alt text](image-6.png)   
![Alt text](image-8.png)   
没有执行。
# 二、写一个三层循环嵌套，分别使用 continue、break 跳出 / 跳转最外层循环。
## 1. continue
![Alt text](image-9.png)   
```text
 continue 代表继续执行，当continue 3 的时候，代表从当前循环向外数第三层，然后继续执行。
```
![Alt text](image-12.png)
## 2. break
![Alt text](image-10.png)   
```text
 break 代表跳出循环，如果和上面一样使用 break 3，那么整个代码循环只会执行一次，因为到最外层（第三层）也被跳出了，
 如果要实现当面的执行效果，这里可以使用 break 2。
```
![Alt text](image-13.png)
# 三、通过 foreach 和 for 循环分别遍历一个数组。
[遍历数组](./array_test.php)   
![Alt text](image-11.png)