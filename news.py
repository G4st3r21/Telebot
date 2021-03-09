from bs4 import BeautifulSoup
from aiogram.utils.markdown import hlink
import requests

last_news = ''


def NewsFrom_MigNewsCom(N):
    url = 'http://mignews.com/mobile'
    page = requests.get(url)
    filteredNews, allNews = [], []

    soup = BeautifulSoup(page.text, "html.parser")
    allNews = soup.findAll('a', class_='lenta')
    allLinks = []
    for link in soup.findAll('a', class_='lenta'):
        allLinks.append('http://mignews.com' + link.get('href'))

    for num, data in enumerate(allNews, start=0):
        if data.find('span', class_='time2'):
            filteredNews.append(hlink(data.text, allLinks[num]))

    return filteredNews[:N]


def Check_for_new_post():
    global last_news
    url = 'http://mignews.com/mobile'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    if last_news != soup.findAll('span', class_='time2')[0]:
        link = soup.findAll('a', class_='lenta')[0]
        text = link.text
        link = 'http://mignews.com' + link.get('href')
        last_news = soup.findAll('span', class_='time2')[0] 
        return hlink(text, link)
