<?php
    session_start();
    include __DIR__.'/db.php';

    $users = $db->prepare("SELECT * FROM `admins`");
    $users->execute();
    $result = $users->FetchAll();
    foreach($result as $admin):
        if($_POST['email'] == $admin['email'])
        {
            $_SESSION['email'] = $_POST['email'];
            if($_POST['password'] == (string)$admin['password'])
            {
                unset($_SESSION['email']);
                $_SESSION['status'] = 'admin';
                header("Location:  /admin_page.php");
                exit();
            }
        }
    endforeach;
    $_SESSION['mes'] = "Неверный email или пароль!";
    header("Location:  /auto.php");
?>