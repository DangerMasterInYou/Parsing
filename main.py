import os
import random
import time
import requests
from fake_useragent import UserAgent
import json
from bs4 import BeautifulSoup


if not os.path.exists("image"):
    os.makedirs("image")

films = []  # Список для хранения фильмов
number = 1


def check_url(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": UserAgent().random
    }
    req = requests.get(url, headers=headers, allow_redirects=False)
    src = req.content
    souper = BeautifulSoup(src, "html.parser")
    return souper


for year in range(2015, 2022+1, 1):
    for month in range(1, 12+1, 1):
        if (year == 2015 and month != 12) or (year == 2020 and 4 <= month <= 8) or (year == 2022 and month >= 7):
            continue
        time.sleep(1)
        page_url = f"https://langal.ru/affiche/{year}-{month}/"
        soup = ""
        for count in range(10 + 1):
            time.sleep(1)
            soup = check_url(page_url)
            if "302 Found" in str(soup):
                print(f"Не удалось {count} раз переадресовать страницу: {page_url}")
                continue
            if "setBlockContent()" in str(soup):
                print(f"Не удалось подключиться {count} раз к странице: {page_url}")
                continue
            break

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
            if div_film.find('td', class_='label', string='Актеры'):
                actors = (div_film.find('td', class_='label', string='Актеры')).find_next_sibling('td').text.strip()
            else:
                actors = "-"

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