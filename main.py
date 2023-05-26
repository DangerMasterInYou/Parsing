import os
import time
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import json


def check_url(date):
    url = f"https://langal.ru/affiche/{date}"
    service = Service('C:\Program Files\JetBrains\PyCharm Community Edition 2023.1.1\chromedriver.exe')
    option = webdriver.ChromeOptions()
    userAgent = UserAgent().random
    option.add_argument(f'user-agent={userAgent}')
    option.add_argument("--disable-extensions")  # Отключение переадресации
    option.add_argument("Cache-Control=no-cache")
    option.add_argument("Pragma=no-cache")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("--disable-web-security")
    option.add_argument("--no-sandbox")
    option.add_argument("Referer=https://langal.ru/affiche/, https://langal.ru/affiche/2022-06")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--disable-gpu")
    option.set_capability('dom.webdriver.enabled', False)
    driver = webdriver.Chrome(service=service, options=option)

    driver.maximize_window()

    try:
        # Добавляем скрипт JavaScript для изменения navigator.webdriver
        script = '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                '''
        driver.execute_script(script)

        driver.get(url=url)
        print(driver.page_source)
        time.sleep(5)
        if "302 Found" in str(driver.find_element_by_tag_name("body")):
            print("Found")
            driver.close()
            check_url(url)
        if "setBlockContent()" in str(driver.find_element_by_tag_name("body")):
            print("setBlockContent()")
            driver.close()
            check_url(url)
        # with open(f"page/date.html", "w") as file:
        #     file.write(driver.page_source)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def main():
    if not os.path.exists("image"):
        os.makedirs("image")
    if not os.path.exists("page"):
        os.makedirs("page")

    films = []  # Список для хранения фильмов

    for year in range(2016, 2022 + 1, 1):
        for month in range(1, 12+1, 1):
            if (year == 2015 and month != 12) or (year == 2020 and 4 <= month <= 8) or (year == 2022 and month >= 7):
                continue
            time.sleep(1)
            date_data = f"{year}-{month}/"
            check_url(date_data)
            # f = open('example.txt', 'r')


if __name__ == "__main__":
    main()

# for year in range(2015, 2022+1, 1):
#     for month in range(1, 12+1, 1):
#         if (year == 2015 and month != 12) or (year == 2020 and 4 <= month <= 8) or (year == 2022 and month >= 7):
#             continue
#         time.sleep(1)
#         page_url = f"https://langal.ru/affiche/{year}-{month}/"
#         soup = check_url(page_url)
#         for count in range(100+1):
#             if "302 Found" in str(soup):
#                 print(f"Не удалось {count} раз переадресовать страницу: {page_url}")
#                 soup = check_url(page_url)
#                 time.sleep(1)
#             if "setBlockContent()" in str(soup):
#                 print(f"Не удалось подключиться {count} раз к странице: {page_url}")
#                 time.sleep(1)
#                 soup = check_url(page_url)
#
#         # Нахождение тегов <div> с классом <filmdesc clear>
#         div_films = soup.find_all("div", class_="filmdesc clear")
#         # Перебор найденных тегов <div>
#         for div_film in div_films:
#             # Нахождение Названия
#             name = (div_film.find("div", class_="film-title")).find("a").text
#
#             # Нахождение Даты проката
#             date_element = div_film.find_all('td', class_='label')
#             start_date = ""
#             end_date = ""
#             for element in date_element:
#                 if 'В прокате' in element.text:
#                     date = element.find_next_sibling('td').text.strip()
#                     if 'по' in date:
#                         start_index = date.index('c') + 2
#                         end_index = date.index('по') - 1
#                         start_date = date[start_index:end_index].strip()
#
#                         start_index = date.index('по') + 3
#                         end_index = date.index('г.', start_index) + 1
#                         end_date = date[start_index:end_index].strip()
#                     else:
#                         start_index = date.index(' ') + 1
#                         end_index = date.index(' г.')
#                         start_date = date[start_index:end_index].strip()
#                         end_date = "-"
#
#             # Нахождение Хронометража
#             duration = div_film.find('td', class_='label', string='Продолжительность')
#             duration = duration.find_next_sibling('td').text.strip()
#
#             # Нахождение Режиссёра
#             director = (div_film.find('td', class_='label', string='Режиссер')).find_next_sibling('td').text.strip()
#
#             # Нахождение Актеров
#             actors = (div_film.find('td', class_='label', string='Актеры')).find_next_sibling('td').text.strip()
#
#             # Нахождение Описания
#             description = div_film.find("div", class_='story').text.strip()
#
#             # Нахождение Постера
#             poster = div_film.find("img")
#             # Получение ссылки на изображение из атрибута "src"
#             img_url = "https://langal.ru/" + poster["src"]
#             # Загрузка изображения
#             img_data = requests.get(img_url).content
#             if img_data:
#                 # Генерация имени файла на основе номера изображения
#                 filename = str(number) + ".jpg"
#                 # Полный путь к файлу
#                 filepath = os.path.join("image", filename)
#                 # Сохранение изображения
#                 with open(filepath, "wb") as f:
#                     f.write(img_data)
#                     # Создание словаря с информацией о фильме
#                     film = {
#                         "Название": name,
#                         "Картинка": filepath,
#                         "Дата_начала_проката": start_date,
#                         "Дата_окончания_проката": end_date,
#                         "Хронометраж": duration,
#                         "Режиссер": director,
#                         "Актеры": actors,
#                         "Описание": description
#                     }
#                     films.append(film)  # Добавление фильма в список
#                     number += 1
#             time.sleep(1)
#         time.sleep(2)
#     time.sleep(3)
#
# # Сохранение данных в файл JSON
# file_mode = "w" if films else "a"
# with open("movies.json", file_mode, encoding="utf-8") as file:
#     json.dump(films, file, ensure_ascii=False, indent=4)


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
# setBlockContent(): Block BANNERS_PLACE3ALL keys mismatch: BLOCK: $VAR1 = {
#           'REQUEST' => {
#                          'place' => '3'
#                        },
#           'MAXAGE' => 300
#         };
#  NEW: $VAR1 = {
#           'MAXAGE' => 300,
#           'REQUEST' => {
#                          'place' => 3
#                        }
#         };