<?php
    $request = array_merge($_GET);
    if(isset($request['token'])){
        $login = unserialize(gzuncompress(base64_decode($request['token'])));
        if($login['user'] === 'test123'){
            echo "flag{xxxxx}";
        }else{
            echo 'unserialize injection!!';
        }
    }