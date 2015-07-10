<?php
    $file_path = htmlspecialchars($_GET['file_path']);
    $file = file($file_path);

    print count($file);
?>
