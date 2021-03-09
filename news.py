from bs4 import BeautifulSoup
from aiogram.utils.markdown import hlink
import requests


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
