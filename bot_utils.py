import bot_data as db
import keys
import requests


def call_city(city):
    # запрашиваем данные по городу на сервере
    web_url = 'https://api.openweathermap.org/geo/1.0/direct'
    answer = requests.get(web_url,
                          params={
                              'q': city,
                              'limit': 1,
                              'appid': keys.app_id
                          }).json()
    return city, answer[0]['lat'], answer[0]['lon']


def call_weather(lat, lon):
    # запрашиваем данные по городу на сервере
    # сервис теперь запрашивает подписку, поэтому сделал заглушку
    web_url = 'https://api.openweathermap.org/data/3.0/onecall'
    # answer = requests.get(web_url,
    #                       params={
    #                           'lat': lat,
    #                           'lon': lon,
    #                           'exclude': 'current',
    #                           'units': 'metric',
    #                           'lang': 'ru',
    #                           'appid': keys.app_id
    #                       }).json()
    # return ((answer[0]['current']['temp'],
            # answer[0]['current']['wind_speed']),
            # answer[0]['current']['weather'][0]['description'])
    return 28.5, 3.13, 'переменная облачность'


if __name__ == '__main__':
    city, lat, lon = call_city('Minsk')
    print(call_weather(lat, lon))

