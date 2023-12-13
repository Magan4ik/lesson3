from typing import NamedTuple

from services.weather.weather_dto import WeatherDTO


class CountryDTO(NamedTuple):
    name: str
    code: str

class CityDTO(NamedTuple):
    id: int
    name: str
    lat: float
    lon: float
    country: CountryDTO
    wiki_page: str
    image: str

class CityInfoDTO(NamedTuple):
    name: str
    lat: float
    lon: float
    country_code: str
    weather_now: WeatherDTO
    weather_forecast: list[WeatherDTO]
    wiki_page: str
    image: str

class CityWeatherDTO(NamedTuple):
    name: str
    lat: float
    lon: float
    country_code: str
    weather_now: WeatherDTO
    weather_forecast: list[WeatherDTO]
