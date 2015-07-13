<?php
  $file_path = htmlspecialchars($_GET['file_path']);
    if(file_exists($file_path)){
        echo htmlspecialchars(file_get_contents($file_path));
    }
?>