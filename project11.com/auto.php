<?php
    session_start();
    include __DIR__.'/db.php';
?>

<!DOCTYPE html>
<html>
<head>
    <title>Авторизация</title>
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

        .form-group input {
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
        <h1>Авторизация</h1>
        <h1><?php echo $_SESSION['mes']; unset($_SESSION['mes']); ?></h1>
        <form method="post" action="autorization.php">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" value="<?php echo $_SESSION['email']; ?>" >
                <label for="password">Пароль</label>
                <input type="password" id="password" name="password" required>
                <button type="submit">Войти</button>
            </div>
        </form>
    </div>
</body>
</html>