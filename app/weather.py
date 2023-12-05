from typing import Tuple, Optional
import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime, timedelta


def convert_unix_to_readable(unix_timestamp: float,
                             timezone_offset: float) -> str:
    # Convert the Unix timestamp to a UTC datetime object
    utc_datetime = datetime.utcfromtimestamp(unix_timestamp)
    # Apply the timezone offset
    local_datetime = utc_datetime + timedelta(seconds=timezone_offset)
    # Format the datetime as a string
    return local_datetime.strftime('%H:%M:%S')


load_dotenv()
API_KEY = os.getenv('API_KEY')


@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: float
    temperatureFeel: float
    temperatureMin: float
    temperatureMax: float
    pressure: float
    humidity: float
    visibility: float
    windSpeed: float
    windDeg: float
    windGust: float
    rainOne: float
    rainThree: float
    snowOne: float
    snowThree: float
    timezone: float
    sunrise: str
    sunset: str
    name: str


def get_lat_long(city_name: str, state_code: str, country_code: str,
                 API_key: Optional[str]) -> Tuple[float, float]:
    if API_key is None:
        raise ValueError("API key is not provided")
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={
                        city_name},{state_code},{country_code}&appid={API_key}'
                        ).json()
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon


def get_current_weather(
        lat: float,
        lon: float,
        API_key: Optional[str]) -> WeatherData:
    if API_key is None:
        raise ValueError("API key is not provided")
    resp = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={
                        lat}&lon={lon}&appid={API_key}&units=imperial').json()

    timezone_offset = resp.get('timezone')

    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=resp.get('main').get('temp'),
        temperatureFeel=resp.get('main').get('feels_like'),
        temperatureMax=resp.get('main').get('temp_max'),
        temperatureMin=resp.get('main').get('temp_min'),
        humidity=resp.get('main').get('humidity'),
        pressure=resp.get('main').get('pressure'),
        visibility=resp.get('visibility'),
        windSpeed=resp.get('wind').get('speed', 0),
        windDeg=resp.get('wind').get('deg', 0),
        windGust=resp.get('wind').get('gust', 0),
        timezone=timezone_offset,
        sunrise=convert_unix_to_readable
        (resp.get('sys').get('sunrise'), timezone_offset),
        sunset=convert_unix_to_readable
        (resp.get('sys').get('sunset'), timezone_offset),
        name=resp.get('name'),

        # Check for rain and snow, default to None or 0 if not present
        rainOne=resp.get('rain', {}).get('1h', 0),
        rainThree=resp.get('rain', {}).get('3h', 0),
        snowOne=resp.get('snow', {}).get('1h', 0),
        snowThree=resp.get('snow', {}).get('3h', 0)
    )
    return data


def main(city_name: str, state_name: str, country_name: str) -> WeatherData:
    lat, lon = get_lat_long(city_name, state_name, country_name, API_KEY)
    weather_data = get_current_weather(lat, lon, API_KEY)
    return weather_data


if __name__ == "__main__":
    city, state, country = 'Grand Junction', 'CO', 'US'
    lat, lon = get_lat_long(city, state, country, API_KEY)
    print(get_current_weather(lat, lon, API_KEY))
