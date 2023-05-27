<?php
    session_start();

    if($_SESSION['status'] != 'admin'){
        die("Вы не администратор!");
    }

    $name = $_GET["name"];
    $jsonData = file_get_contents('movies.json');
    $movies = json_decode($jsonData, true);

    // Поиск фильма по имени и удаление его
    foreach ($movies as $key => $movie) {
        if ($movie['Название'] == $name) {
            // Удаление изображения
            $imagePath = 'image/' . $movie['Картинка'];
            if (file_exists($imagePath)) {
                unlink($imagePath);
            }

            // Удаление фильма из массива
            unset($movies[$key]);
            break;
        }
    }

    // Преобразование массива обратно в JSON
    $updatedJsonData = json_encode($movies, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);

    // Запись обновленных данных в файл
    file_put_contents('movies.json', $updatedJsonData);

    $_SESSION['mes']="Удалено!";
    header("Location:  /admin_page.php");
?>