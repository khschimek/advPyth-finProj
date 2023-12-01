# Geocoding API
# https://openweathermap.org/api/geocoding-api
# Current Weather Data API
# https://openweathermap.org/current#data


import requests
from decouple import config
from dataclasses import dataclass


@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: str


API_KEY = config('API_KEY', default='YOUR_DEFAULT_API_KEY')


def get_lat_long(city_name, state_code, country_code, API_key):
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={
                        city_name},{state_code},{country_code}&appid={API_key}'
                        ).json()

    data = resp[0]
    lat, long = data.get('lat'), data.get('lon')
    return lat, long


def get_current_weather(lat, long, API_key):
    resp = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={
                        lat}&lon={long}&appid={API_key}&units=imperial').json()
    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=resp.get('main').get('temp')
    )
    return data


def main(city_name, state_name, country_name):
    lat, long = get_lat_long('Grand Junction', 'CO', 'US', API_KEY)
    weather_data = get_current_weather(lat, long, API_KEY)
    return weather_data


if __name__ == "__main__":
    lat, lon = get_lat_long('Grand Junction', 'CO', 'US', API_KEY)
    print(get_current_weather(lat, lon, API_KEY))
