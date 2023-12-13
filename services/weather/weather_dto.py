from typing import NamedTuple

class CoordinatesDTO(NamedTuple):
    lat: float
    lon: float

class WeatherCityDTO(NamedTuple):
    name: str
    country_code: str
    coordinates: CoordinatesDTO

class TemperatureDTO(NamedTuple):
    normal: float
    feel: float
    min: float
    max: float

class TimeDTO(NamedTuple):
    current: str
    sunrise: str
    sunset: str

class WeatherDTO(NamedTuple):
    city: WeatherCityDTO
    city_id: int
    weather: str
    description: str
    temperature: TemperatureDTO
    humidity: int
    wind_speed: float
    wind_direction: str
    icon_url: str
    time: TimeDTO


