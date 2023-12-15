<?php
$array = array("1","2","3") ;
$count = count($array);
for ($i = 0; $i < $count; $i++) {
    echo"". $array[$i] ."\n";
}
foreach ($array as $key => $value) {
    echo "". $key ."=>";
    echo "". $value ."\n";
}