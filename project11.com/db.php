<?php
    define('DB_DRIVER', 'mysql');
    define('DB_HOST', 'localhost');
    define('DB_NAME', 'adminKinodb');
    define('DB_USER', 'root');
    define('DB_PASSWORD', '');

    try{
        $db = new PDO(DB_DRIVER.':host='.DB_HOST.';dbname='.DB_NAME, DB_USER, DB_PASSWORD);
    }
    catch(PDOException $ex){
        die("Could not connect to the database $dbname :" . $ex->getMessage());
    }
?>