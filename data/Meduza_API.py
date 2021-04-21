from aiogram.utils.markdown import hlink
import requests


def NewsFromMeduza(N):
    ans = requests.get(
        'https://meduza.io/api/v3/search?chrono=news&page=0&per_page=10&locale=ru')
    ans = ans.json()

    news = []
    for i in ans['documents']:
        news.append(hlink(ans['documents'][i]['title'],
                          ans['documents'][i]['url']))

    # for i in range(10):
    #     print(news[i], urls[i], sep='\n', end='\n\n')

    return news[:N]
