<?php
// i循环三次，预期j,k永远为0，且只执行一次
for ($i = 0; $i < 3; $i++) {
    echo("第一层循环i为" . $i ."\n");
    for ($j = 0; $j < 3; $j++) {
        echo("第二层循环j为" . $j ."\n");
        for ($k = 0; $k < 3; $k++) {
            echo("第三层循环k为" . $k ."\n");
                continue 3;            
        }
    }
}