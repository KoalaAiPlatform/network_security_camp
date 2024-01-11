<?php
if($_GET["id"]) {
$id = intval($_GET["id"]);
if ($_GET["id"]==1024) {
    echo "<p>no! try again</p>";
}
else if($id == 1024){
    echo "flag{xxxxx}";
 }
}
?>