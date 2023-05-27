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
    <title>Редактирование</title>
    <style>
        body {
            background-color: #f4f4f4;
            font-family: Arial, sans-serif;
        }

        .container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .form-group input,
        .form-group textarea {
            width: 95%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
            margin-bottom: 5px;
        }

        .form-group button {
            width: 100%;
            padding: 10px;
            background-color: #124e20;
            color: #fff;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        .form-group button:hover {
            background-color: #0c3c16;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Редактирование</h1>
        <form method="post" action="editing.php">
            <div class="form-group">
                <label for="name">Название</label>
                <input type="text" id="name" name="name" value="<?php echo rawurldecode($_GET['name']) ?>">
                <label for="description">Описание</label>
                <textarea id="description" name="description"><?php
                    // Загрузка данных из файла JSON
                    $jsonData = file_get_contents('movies.json');
                    $films = json_decode($jsonData, true);
                    $name = rawurldecode($_GET['name']);

                    foreach ($films as $key => $movie) {
                        if ($movie['Название'] == $name) {
                            echo $movie['Описание'];
                        }
                    }
                ?></textarea>
                <button type="submit">Edit</button>
            </div>
        </form>
    </div>
</body>
</html>
