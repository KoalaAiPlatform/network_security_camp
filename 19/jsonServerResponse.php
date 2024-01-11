<?php
$call_method = $_GET['jsonp'];
echo $call_method . "({msg: 'json data'})";