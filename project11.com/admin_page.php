<?php
    session_start();
    include __DIR__.'/db.php';
    if($_SESSION['status'] != 'admin'){
        die("Вы не администратор!");
    }
?>
<!DOCTYPE html>
<html>
<head>
    <title>Список фильмов</title>
    <style>
        header {
            background-color: #333;
            color: #fff;
            display: flex;
        }

        .logo {
            flex-shrink: 0;
            width: 70px;
            height: 70px;
            margin-right: 27px;
            padding: 10px;
            display: flex;
        }

        .container {
            max-width: 960px;
            margin: 0;
            vertical-align: middle;
            margin-top: 10px;
        }

        .auth-container {
            margin-left: auto;
            margin-right: 20px;
        }

        .auth-button {
            margin-top: 20px;
            padding: 10px 20px;
            color: #124e20;
            background-color: #d3d5bd;
            font-weight: bold;
            border: none;
            border-radius: 4px;
        }

        .auth-button:hover {
            color: black;
            background-color: #fff;
        }

        h1 {
            margin: 0;
            font-size: 28px;
            font-weight: bold;
        }

        p {
            margin: 0;
            font-size: 18px;
        }

        a {
          text-decoration: none;
          display: inline-block;
          text-align: center;
          line-height: 2;
          background-color: yellow;
          border-radius: 20px;
        }

        a:hover {
          color: black;
          background-color: red;
          border-radius: 20px;
        }

        body {
            padding: 0;
            font-family: Arial, sans-serif;
            background-image: url("img_css/body.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }

        .film-container {
            display: flex;
            align-items: flex-start;
            margin-bottom: 20px;
            padding: 10px;
            background-image: url("img_css/film_container.jpg");
            background-size: cover;
            background-position: center;
        }

        .film-image {
            flex-shrink: 0;
            width: 190px;
            height: 269px;
            margin-right: 20px;
        }

        .film-details {
            flex-grow: 1;
        }

        .film-title {
            text-align: center;
            color:#2577dd;
            font-size: 25px;
            font-weight: bold;
            margin-bottom: 10px;
            border-top: 5px solid #fff;
            border-bottom: 5px solid #fff;
        }
        .ud {
            float: right;
            align-items: center;
            color:#124e20;
            font-size: 19px;
            font-weight: bold;
        }

        .film-info {
            margin-bottom: 10px;
            font-size: 14px;
        }

        .film-description {
            font-style: italic;
            font-size: 16px;
            line-height: 1.4;
                color:#e7e9d5;
        }

        .search-container {
            margin-bottom: 20px;
            margin-top: 10px;
            margin-left: 10px;
        }

        .search-input {
            width: 300px;
            padding: 5px;
            font-size: 14px;
        }
    </style>
</head>

<header>
    <div class="logo">
        <img src="img_css/logo.jpg">
    </div>
    <div class="container">
        <h1>Список фильмов</h1>
        <p>Найдите свой любимый фильм</p>
        <p>
            <?php
                echo $_SESSION['mes'];
                unset($_SESSION['mes']);
            ?>
        </p>
    </div>
    <div class="auth-container">
        <form action="/exit.php" method="POST" enctype="multipart/form-data">
            <button class="auth-button" name="exit">Выход</button>
        </form>
    </div>
</header>

<body>
    <div class="search-container">
        <form method="get" action="">
            <input type="text" name="search" class="search-input" placeholder="Поиск по названию" value="<?php echo isset($_GET['search']) ? $_GET['search'] : ''; ?>">
            <button type="submit">Найти</button>
        </form>
    </div>

    <?php

        // Загрузка данных из файла JSON
        $jsonData = file_get_contents('movies.json');
        $films = json_decode($jsonData, true);

        // Функция для фильтрации фильмов по названию
        function filterFilms($films, $search)
        {
            if (empty($search)) {
                return $films;
            }
            $filteredFilms = array();
            foreach ($films as $film) {
                if (stripos($film['Название'], $search) !== false) {
                    $filteredFilms[] = $film;
                }
            }
            return $filteredFilms;
        }

        // Получение значения поиска из GET-параметров
        $search = isset($_GET['search']) ? $_GET['search'] : '';

        // Фильтрация фильмов по названию
        $filteredFilms = filterFilms($films, $search);

        // Перебор отфильтрованных фильмов и вывод информации
        foreach ($filteredFilms as $film) {
            echo '<div class="film-container">';
            echo '<div class="film-image"><img src="' . $film['Картинка'] . '"></div>';
            echo '<div class="film-details">';
            echo '<div class="film-title">' . $film['Название'] . "</div>";
            echo '<div class=""><a href="edit.php?name=' . urlencode($film['Название']) . '">Редактировать</a>&nbsp';
            echo '<a href="ud.php?name=' . urlencode($film['Название']) .  '">Удалить</a></div>';
            echo '<div class="film-info">Дата начала проката: ' . $film['Дата_начала_проката'] . '</div>';
            echo '<div class="film-info">Дата окончания проката: ' . $film['Дата_окончания_проката'] . '</div>';
            echo '<div class="film-info">Хронометраж: ' . $film['Хронометраж'] . '</div>';
            echo '<div class="film-info">Режиссер: ' . $film['Режиссер'] . '</div>';
            echo '<div class="film-info">Актеры: ' . $film['Актеры'] . '</div>';
            echo '<div class="film-description">' . $film['Описание'] . '</div>';
            echo '</div>';
            echo '</div>';
        }
    ?>
</body>
</html>
