from .config import weather_api_key
import requests


s_city = "Voronezh,RU"
city_id = 472045
appid = weather_api_key

def WeatherCheck():
    weather = []
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                        params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()

        weather.append(f'\n\tСейчас: {data["weather"][0]["description"]}')
        weather.append(f'\n\tТемпература: {data["main"]["temp"]}°')
        weather.append(f'\n\tПо ощущению: {data["main"]["feels_like"]}°')

        return weather
    except Exception as e:
        print("Exception (find):", e)
