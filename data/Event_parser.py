from asyncio import events
from os import sep
from google.api_core.exceptions import AlreadyExists
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestsDependencyWarning

def Yandex_Afisha_events():

    url = 'https://afisha.yandex.ru/voronezh?preset=today'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup.get_text(' '))
    events = soup.find_all('h2', class_='Title-sc-5meihc-3 dgYFQo')
    img = soup.find_all('img', class_='ImageBackground-sc-7hy03b-1 kCvqAF')
    
    return [event.get_text("|").split("|") for event in events]

def Afisha_ru_films():

    url = 'https://www.afisha.ru/voronezh/cinema/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    films = soup.find_all('h2', class_='tile__title')
    films_genres = soup.find_all('span', class_='tile__badge')
    films_descriptions = soup.find_all('p', class_='tile__description')
    films_links = soup.find_all('a', class_='tile__link')

    # print(films, films_genres, films_descriptions, films_links, sep='\n\n')

    films = [film.get_text("|").split("|") for film in films]
    films_genres = [films_genre.get_text("|").split("|") for films_genre in films_genres]
    films_descriptions = [films_description.get_text("|").split("|") for films_description in films_descriptions]
    films_links = [films_link.get('href') for films_link in films_links]
    # print(films, films_genres, films_descriptions, films_links, sep='\n\n')
    AllInfo = []
    for _ in range(len(films)):
        AllInfo.append([films[_], films_genres[_], films_descriptions[_], films_links[_]])
    
    Endstrk = ''

    for i in range(len(films)):
        Endstrk += f'Название: {films[i][0]}\n\n'
        Endstrk += f'Жанр: {films_genres[i][0]}\n\n'
        Endstrk += f'Описание: {films_descriptions[i][0]}\n\n'
        Endstrk += f'Подробнее: https://www.afisha.ru/{films_links[i][1:]}'
        Endstrk += '\n\n-------------------------------------------\n\n'
    
    return Endstrk



# Надо проверять кино/квест по ключевым словам и выводить красиво, в идеале с картинкой(?)

# Events = Yandex_Afisha_events()
# End_Events = []
# for event in Events:

#     End_Events.append('|'.join(event))
# print(End_Events)
# with open('data/Events.txt', 'w') as file:
#     file.writelines(End_Events)

