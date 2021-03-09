from bs4 import BeautifulSoup
import requests

def NewsFrom_MigNewsCom(N):
    url = 'http://mignews.com/mobile'
    page = requests.get(url)
    filteredNews, allNews = [], []
    print(page.status_code)

    soup = BeautifulSoup(page.text, "html.parser")
    allNews = soup.findAll('a', class_='lenta')

    for data in allNews:
        if data.find('span', class_='time2') is not None:
            filteredNews.append(data.text)
    
    return filteredNews[:N]
