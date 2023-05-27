<?php
    session_start();

    if ($_SESSION['status'] != 'admin') {
        die("Вы не администратор!");
    }

    $name = $_POST["name"];
    $newDescription = $_POST["description"];

    $jsonData = file_get_contents('movies.json');
    $movies = json_decode($jsonData, true);

    // Поиск фильма по имени и изменение описания
    foreach ($movies as $key => &$movie) {
        if ($movie['Название'] == $name) {
            // Изменение описания фильма
            $movie['Описание'] = $newDescription;
            break;
        }
    }

    // Преобразование массива обратно в JSON
    $updatedJsonData = json_encode($movies, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);

    // Запись обновленных данных в файл
    file_put_contents('movies.json', $updatedJsonData);

    $_SESSION['mes'] = "Описание изменено!";
    header("Location: /admin_page.php");
?>
