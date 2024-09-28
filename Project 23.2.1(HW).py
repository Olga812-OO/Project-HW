import requests
from bs4 import BeautifulSoup

import pandas as pd

def collect_user_rates(user_login):
    page_num = 1

    data = []

    while True:
        url = f'https://www.kinopoisk.ru/user/{user_login}/votes/list/vs/vote/page/{page_num}'
        html_content = requests.get(url).text

        soup = BeautifulSoup(html_content, 'lxml')

        # Находим все элементы <div> с классом item
        entries = soup.find_all('div', class_='item')

        # Признак остановки
        if len(entries) == 0:
            break

        for entry in entries:
            # Ищем элемент <div> с классом 'nameRus'
            div_nameRus = entry.find('div', class_='nameRus')
            # Теперь, внутри div_nameRus ищем элемент <a> и получаем его текстовое содержимое методом .text:
            film_name = div_nameRus.find('a').text

            # Находим элемент div класса date и получаем текстовое представление
            release_date = entry.find('div', class_='date').text

            # Находим элемент div класса rating:
            div_rating = entry.find('div', class_='rating')
            # Теперь, внутри div_rating ищем элемент <b> и получаем его текстовое содержимое методом .text:
            rating = div_rating.find('b').text

            data.append({'film_name': film_name, 'release_date': release_date, 'rating': rating})

            page_num += 1  # Переходим на следующую страницу

        return data

user_rates = collect_user_rates(input("Введите логин: "))
print(len(user_rates))

df = pd.DataFrame(user_rates)
df.to_excel('user_rates.xlsx')
print(df)
