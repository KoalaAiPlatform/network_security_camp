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