<?php
  $file_path = htmlspecialchars($_GET['file_path']);
    if(file_exists($file_path)){
        readfile($file_path);
    }
?>