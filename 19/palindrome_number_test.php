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
# intval() 函数⽤于获取变量的整数值
# strval() 函数⽤于获取变量的字符串值
# strrev() 函数反转字符串
?>