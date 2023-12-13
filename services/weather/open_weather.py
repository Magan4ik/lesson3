import requests
import datetime

from services import services_config
from services.service_interfaces import WeatherTodayInterface, WeatherForecastInterface
from services.weather.exceptions import ServerInvalidResponseError, CityNotFoundError, ServerReturnInvalidStatusCode
from services.weather.weather_dto import WeatherDTO, WeatherCityDTO, CoordinatesDTO, TemperatureDTO, TimeDTO


def degrees_to_wind_direction(degrees: int) -> str:
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

    # Перевод угла в направление
    index = round(degrees / (360. / len(directions))) % len(directions)
    return directions[index]


class OpenWeatherTodayService(WeatherTodayInterface):
    _appid = services_config.get_openweather_appid()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather"

    @classmethod
    def get_weather(cls, city: str) -> WeatherDTO:
        response = cls._get_weather_json_by_name(city=city)
        status_code = int(response['cod'])
        cls._validate_response_or_raise(response, status_code)
        weather_dto = cls._parse_json_to_weather_dto(response)
        return weather_dto

    @classmethod
    def get_weather_by_id(cls, city_id: int) -> WeatherDTO:
        response = cls._get_weather_json_by_id(city_id=city_id)
        status_code = int(response['cod'])
        cls._validate_response_or_raise(response, status_code)
        weather_dto = cls._parse_json_to_weather_dto(response)
        return weather_dto

    @classmethod
    def _get_weather_json_by_name(cls, city: str, lang="en") -> dict:
        response = requests.get(cls.current_weather_url,
                                params={"q": city, "appid": cls._appid, "units": "metric", "lang": lang},
                                timeout=(cls.connect_timeout, cls.read_timeout))
        weather_json = response.json()
        return weather_json

    @classmethod
    def _get_weather_json_by_id(cls, city_id: int, lang="en") -> dict:
        response = requests.get(cls.current_weather_url,
                                params={"id": city_id, "appid": cls._appid, "units": "metric", "lang": lang},
                                timeout=(cls.connect_timeout, cls.read_timeout))
        weather_json = response.json()
        return weather_json

    @staticmethod
    def _parse_json_to_weather_dto(json_response: dict) -> WeatherDTO:
        city = WeatherCityDTO(
            name=json_response['name'],
            country_code=json_response['sys']['country'],
            coordinates=CoordinatesDTO(
                lat=json_response['coord']['lat'],
                lon=json_response['coord']['lon']
            )
        )
        city_id = json_response['id']
        weather = json_response['weather'][0]['main']
        description = json_response['weather'][0]['description']
        temperature = TemperatureDTO(
            normal=json_response['main']['temp'],
            feel=json_response['main']['feels_like'],
            min=json_response['main']['temp_min'],
            max=json_response['main']['temp_max']
        )
        humidity = json_response['main']['humidity']
        wind_speed = int(json_response['wind']['speed'] * 3.6)
        wind_direction = degrees_to_wind_direction(json_response['wind']['deg'])
        icon_url = f"https://openweathermap.org/img/wn/{json_response['weather'][0]['icon']}@2x.png"
        time = TimeDTO(
            current=datetime.datetime.fromtimestamp(json_response['dt']).strftime('%H:%M'),
            sunrise=datetime.datetime.utcfromtimestamp(
                json_response['sys']['sunrise'] + json_response['timezone']).strftime('%H:%M'),
            sunset=datetime.datetime.utcfromtimestamp(
                json_response['sys']['sunset'] + json_response['timezone']).strftime('%H:%M')
        )
        weather_dto = WeatherDTO(
            city=city,
            city_id=city_id,
            weather=weather,
            description=description,
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            icon_url=icon_url,
            time=time
        )
        return weather_dto

    @staticmethod
    def _validate_response_or_raise(response_json: dict, status_code: int):
        if response_json is None:
            raise ServerInvalidResponseError(f'OpenWeather internal server error, status code: {status_code}')

        if status_code != 200:
            if status_code == 404:
                raise CityNotFoundError(response_json['message'].capitalize())
            raise ServerReturnInvalidStatusCode(f'OpenWeather return invalid status code, status code: {status_code}')

class OpenWeatherForecastService(WeatherForecastInterface):
    _appid = services_config.get_openweather_appid()
    forecast_weather_url = "https://api.openweathermap.org/data/2.5/forecast"

    @classmethod
    def get_weather(cls, city: str, cnt=5, lang="en") -> list[WeatherDTO]:
        response = cls._get_forecast_json_by_name(city=city, cnt=cnt, lang=lang)
        status_code = int(response['cod'])
        cls._validate_response_or_raise(response, status_code)
        forecast_list = cls._parse_forecast_json_to_weather_dto(response)
        return forecast_list

    @classmethod
    def get_weather_by_id(cls, city_id: int, cnt=5, lang="en") -> list[WeatherDTO]:
        response = cls._get_forecast_json_by_id(city_id=city_id, cnt=cnt, lang=lang)
        status_code = int(response['cod'])
        cls._validate_response_or_raise(response, status_code)
        forecast_list = cls._parse_forecast_json_to_weather_dto(response)
        return forecast_list

    @classmethod
    def _get_forecast_json_by_name(cls, city: str, cnt=5, lang="en") -> dict:
        response = requests.get(cls.forecast_weather_url,
                                params={"q": city, "appid": cls._appid, "units": "metric", "lang": lang, "cnt": cnt},
                                timeout=(cls.connect_timeout, cls.read_timeout))
        weather_json = response.json()
        return weather_json

    @classmethod
    def _get_forecast_json_by_id(cls, city_id: int, cnt=5, lang="en") -> dict:
        response = requests.get(cls.forecast_weather_url,
                                params={"id": city_id, "appid": cls._appid, "units": "metric", "lang": lang, "cnt": cnt},
                                timeout=(cls.connect_timeout, cls.read_timeout))
        weather_json = response.json()
        return weather_json

    @staticmethod
    def _parse_forecast_json_to_weather_dto(json_response: dict) -> list[WeatherDTO]:
        forecast_list = list()
        for data in json_response['list']:
            city = WeatherCityDTO(
                name=json_response['city']['name'],
                country_code=json_response['city']['country'],
                coordinates=CoordinatesDTO(
                    lat=json_response['city']['coord']['lat'],
                    lon=json_response['city']['coord']['lon']
                )
            )
            city_id = json_response['city']['id']
            weather = data['weather'][0]['main']
            description = data['weather'][0]['description']
            temperature = TemperatureDTO(
                normal=data['main']['temp'],
                feel=data['main']['feels_like'],
                min=data['main']['temp_min'],
                max=data['main']['temp_max']
            )
            humidity = data['main']['humidity']
            wind_speed = int(data['wind']['speed'] * 3.6)
            wind_direction = degrees_to_wind_direction(data['wind']['deg'])
            icon_url = f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            time = TimeDTO(
                current=datetime.datetime.fromtimestamp(data['dt']).strftime('%H:%M'),
                sunrise=datetime.datetime.utcfromtimestamp(
                    json_response['city']['sunrise'] + json_response['city']['timezone']).strftime('%H:%M'),
                sunset=datetime.datetime.utcfromtimestamp(
                    json_response['city']['sunset'] + json_response['city']['timezone']).strftime('%H:%M')
            )
            weather_dto = WeatherDTO(
                city=city,
                city_id=city_id,
                weather=weather,
                description=description,
                temperature=temperature,
                humidity=humidity,
                wind_speed=wind_speed,
                wind_direction=wind_direction,
                icon_url=icon_url,
                time=time
            )
            forecast_list.append(weather_dto)
        return forecast_list

    @staticmethod
    def _validate_response_or_raise(response_json: dict, status_code: int):
        if response_json is None:
            raise ServerInvalidResponseError(f'OpenWeather internal server error, status code: {status_code}')

        if status_code != 200:
            if status_code == 404:
                raise CityNotFoundError(response_json['message'].capitalize())
            raise ServerReturnInvalidStatusCode(f'OpenWeather return invalid status code, status code: {status_code}')
