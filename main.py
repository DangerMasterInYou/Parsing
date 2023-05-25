import os
import time
import requests
import json
from bs4 import BeautifulSoup

if not os.path.exists("image"):
    os.makedirs("image")

films = []  # Список для хранения фильмов
number = 1
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}
proxies = {
    'http': 'https://185.15.172.212:3128'
}


def check_url(url):
    req = requests.get(url, headers=headers, allow_redirects=False)
    src = req.content
    soup = BeautifulSoup(src, "html.parser")
    return soup


for year in range(2015, 2022+1, 1):
    for month in range(1, 12+1, 1):
        if (year == 2015 and month != 12) or (year == 2020 and 4 <= month <= 8) or (year == 2022 and month >= 7):
            continue
        time.sleep(1)
        page_url = f"https://langal.ru/affiche/{year}-{month}/"
        soup = check_url(page_url)
        for count in range(100+1):
            if "302 Found" in str(soup):
                print(f"Не удалось {count} раз переадресовать страницу: {page_url}")
                soup = check_url(page_url)
                time.sleep(1)
            if "setBlockContent()" in str(soup):
                print(f"Не удалось подключиться {count} раз к странице: {page_url}")
                time.sleep(1)
                soup = check_url(page_url)

        # Нахождение тегов <div> с классом <filmdesc clear>
        div_films = soup.find_all("div", class_="filmdesc clear")
        # Перебор найденных тегов <div>
        for div_film in div_films:
            # Нахождение Названия
            name = (div_film.find("div", class_="film-title")).find("a").text

            # Нахождение Даты проката
            date_element = div_film.find_all('td', class_='label')
            start_date = ""
            end_date = ""
            for element in date_element:
                if 'В прокате' in element.text:
                    date = element.find_next_sibling('td').text.strip()
                    if 'по' in date:
                        start_index = date.index('c') + 2
                        end_index = date.index('по') - 1
                        start_date = date[start_index:end_index].strip()

                        start_index = date.index('по') + 3
                        end_index = date.index('г.', start_index) + 1
                        end_date = date[start_index:end_index].strip()
                    else:
                        start_index = date.index(' ') + 1
                        end_index = date.index(' г.')
                        start_date = date[start_index:end_index].strip()
                        end_date = "-"

            # Нахождение Хронометража
            duration = div_film.find('td', class_='label', string='Продолжительность')
            duration = duration.find_next_sibling('td').text.strip()

            # Нахождение Режиссёра
            director = (div_film.find('td', class_='label', string='Режиссер')).find_next_sibling('td').text.strip()

            # Нахождение Актеров
            actors = (div_film.find('td', class_='label', string='Актеры')).find_next_sibling('td').text.strip()

            # Нахождение Описания
            description = div_film.find("div", class_='story').text.strip()

            # Нахождение Постера
            poster = div_film.find("img")
            # Получение ссылки на изображение из атрибута "src"
            img_url = "https://langal.ru/" + poster["src"]
            # Загрузка изображения
            img_data = requests.get(img_url).content
            if img_data:
                # Генерация имени файла на основе номера изображения
                filename = str(number) + ".jpg"
                # Полный путь к файлу
                filepath = os.path.join("image", filename)
                # Сохранение изображения
                with open(filepath, "wb") as f:
                    f.write(img_data)
                    # Создание словаря с информацией о фильме
                    film = {
                        "Название": name,
                        "Картинка": filepath,
                        "Дата_начала_проката": start_date,
                        "Дата_окончания_проката": end_date,
                        "Хронометраж": duration,
                        "Режиссер": director,
                        "Актеры": actors,
                        "Описание": description
                    }
                    films.append(film)  # Добавление фильма в список
                    number += 1
            time.sleep(1)
        time.sleep(2)
    time.sleep(3)

# Сохранение данных в файл JSON
file_mode = "w" if films else "a"
with open("movies.json", file_mode, encoding="utf-8") as file:
    json.dump(films, file, ensure_ascii=False, indent=4)


        #     # Нахождение тегов <div> с классом <img>
        #     div_tags = soup.find_all("div", class_="img")
        #     # Перебор найденных тегов <div>
        #     for div_tag in div_tags:
        #         # Поиск всех тегов <a> внутри текущего тега <div>
        #         a_tags = div_tag.find_all("a")
        #
        #         # Перебор найденных тегов <a>
        #         for a_tag in a_tags:
        #             # Поиск тегов <img> внутри текущего тега <a>
        #             img_tags = a_tag.find_all("img")
        #
        #             # Перебор найденных тегов <img>
        #             for img_tag in img_tags:
        #                 # Получение ссылки на изображение из атрибута "src"
        #                 img_url = "https://langal.ru/" + img_tag["src"]
        #
        #                 # Загрузка изображения
        #                 img_data = requests.get(img_url).content
        #
        #                 time.sleep(1)
        #
        #                 if img_data:
        #                     # Генерация имени файла на основе номера изображения
        #                     filename = str(number)
        #
        #                     # Полный путь к файлу
        #                     filepath = os.path.join("image", filename)
        #
        #                     # Сохранение изображения
        #                     with open(filepath, "wb") as f:
        #                         f.write(img_data)
        #                 else:
        #                     print(f"Не удалось загрузить изображение: {img_url}")
        #
        #                 # Создание словаря с информацией о фильме
        #                 film = {
        #                     "Название": name,  # Заполните нужные значения
        #                     "Картинка": filepath,
        #                     "Дата_начала_проката": "",  # Заполните нужные значения
        #                     "Дата_окончания_проката": "",  # Заполните нужные значения
        #                     "Хронометраж": "",  # Заполните нужные значения
        #                     "Режиссер": "",  # Заполните нужные значения
        #                     "Актеры": "",  # Заполните нужные значения
        #                     "Описание": ""  # Заполните нужные значения
        #                 }
        #                 films.append(film)  # Добавление фильма в список
        #                 number += 1
        #     time.sleep(1)
        # time.sleep(1)

    #     # Нахождение тегов <div> с классом <img>
    #     div_tags = soup.find_all("div", class_="img")
    #     # Перебор найденных тегов <div>
    #     for div_tag in div_tags:
    #         # Поиск всех тегов <a> внутри текущего тега <div>
    #         a_tags = div_tag.find_all("a")
    #
    #         # Перебор найденных тегов <a>
    #         for a_tag in a_tags:
    #             # Поиск тегов <img> внутри текущего тега <a>
    #             img_tags = a_tag.find_all("img")
    #
    #             # Перебор найденных тегов <img>
    #             for img_tag in img_tags:
    #                 # Получение ссылки на изображение из атрибута "src"
    #                 img_url = "https://langal.ru/" + img_tag["src"]
    #
    #                 # Загрузка изображения
    #                 img_data = requests.get(img_url).content
    #
    #                 time.sleep(1)
    #
    #                 if img_data:
    #                     # Генерация имени файла на основе номера изображения
    #                     filename = str(number)
    #
    #                     # Полный путь к файлу
    #                     filepath = os.path.join("image", filename)
    #
    #                     # Сохранение изображения
    #                     with open(filepath, "wb") as f:
    #                         f.write(img_data)
    #                 else:
    #                     print(f"Не удалось загрузить изображение: {img_url}")
    #
    #                 # Создание словаря с информацией о фильме
    #                 film = {
    #                     "Название": "",  # Заполните нужные значения
    #                     "Картинка": filepath,
    #                     "Дата_начала_проката": "",  # Заполните нужные значения
    #                     "Дата_окончания_проката": "",  # Заполните нужные значения
    #                     "Хронометраж": "",  # Заполните нужные значения
    #                     "Режиссер": "",  # Заполните нужные значения
    #                     "Актеры": "",  # Заполните нужные значения
    #                     "Описание": ""  # Заполните нужные значения
    #                 }
    #                 films.append(film)  # Добавление фильма в список
    #                 number+=1
    #     time.sleep(1)
    # time.sleep(1)





        # films_page = soup.find_all(class_='filmdesc clear')
        # for film in films_page:
        #     film_title = films_page.find('div', class_='film-title').find('a').text.strip()
        #
        #     film_data = [film_title, ]
        #     films_data.append(film_data)

# for film in films_data:
#     film_title = film.find('div', class_='film-title').find('a').text.strip()
#     print(film_title)

        # with open("films.html", "w") as file:
        #     file.write(formatted_src)
