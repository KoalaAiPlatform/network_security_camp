<?php
if(mb_ereg("password",$_GET['id'])) {
    echo("<p>not allowed!</p>");
    exit();
}
$_GET['id'] = urldecode($_GET['id']);
if($_GET['id'] == "password")
{
    echo "<p>Access granted!</p>";
    echo "<p>flag: This is flag!!!} </p>";
}
?>