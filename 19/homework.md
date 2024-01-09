# 一、复现所有 PHP 函数特有漏洞。
## 1. `extract` 变量覆盖
### 1.1 `extract` 函数说明
函数从数组中将变量导入到当前的变量表。该函数使用数组键名作为变量名，使用数组键值作为变量值。**如果有冲突，覆盖已有的变量**。
### 1.2 小题
```php
 <?php
 $magedu = 'extract_file.txt';
 extract($_GET);
 if (isset($student)) {
    $content = trim(file_get_contents($magedu));
    if ($student == $content) {
        echo 'falg{xxxxx}';
    } else {
        echo 'ERROR';
    }
 }
```
**代码说明：**首先将 `extract_file.txt` 赋值给 `$magedu` 变量，然后获取 `$student` 变量的值，如果和 `extract_file.txt` 文件中内容一致，则拿到 `flag`。   
**解题思路：**基于`extract()`函数的变量覆盖的特性，GET请求中，将 `$magedu` 变量重新赋值，`$student` 变量不给值，使得下面的判断为 `NULL == NULL`,满足条件后拿到`flag`。   
![Alt text](image.png)   
**poc：**   
```url
 http://localhost:3000/19/extract_test.php?magedu=123&student=
```
## 2. 绕过过滤的空⽩字符
### 2.1 空白字符
可以引⼊\f（也就是%0c）在数字前⾯，来绕过最后那个is_palindrome_number函数，⽽对于前⾯的数字判断，因为`intval`会忽略这个字符，所以不会影响。   
![Alt text](image-2.png)   
`trim()`函数不过滤 `%0C`,但是`intval`会忽略，而 `' 191'=='191'` 比较时，两边都会进行数值转换，所以会返回true。
### 2.2 小题
```php
 <?php
    function is_palindrome_number($number) {
        $number = strval($number); //strval — 获取变量的字符串值
        $i = 0;
        $j = strlen($number) - 1; //strlen — 获取字符串⻓度
        while($i < $j) {
            if($number[$i] !== $number[$j]) {
            return false;
        }
            $i++;
            $j--;
        }
        return true;
    }
    # trim() 函数移除字符串两侧的空⽩字符或其他预定义字符
    $a = trim($_GET['number']);
    if(($a==strval(intval($a)))&
    (intval($a)==intval(strrev($a)))&!is_palindrome_number($a)){
        echo 'flag{xxxxx}';
    }
```
**说明：**想要拿到`flag`需要满足：（1）`$a==strval(intval($a))` a 为纯数字；（2）`intval($a)==intval(strrev($a))` a反转后和原来的值相等；（3）`!is_palindrome_number($a)` 不是一个回文数
**解题思路：**可以在参数前面添加一个空格，使得第一个第二个条件中在`intval()`函数处理过程中忽略，而在第三个条件中字符挨个比对时，又会被正常检测，所以可以在变量前加个 `%0C` 空白字符来绕过。   
![Alt text](image-1.png)
**poc：**   
```url
 http://localhost:3000/19/palindrome_number_test.php?number=%0C191
```

# 二、复现 jsonp 劫持漏洞。
# 三、复现课件中 Java 多态代码。