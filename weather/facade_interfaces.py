from abc import ABCMeta, abstractmethod

from services.weather.weather_dto import WeatherDTO
from weather.dtos import CityInfoDTO, CityWeatherDTO, CountryDTO


class CityInfoFacadeInterface(metaclass=ABCMeta):

    @abstractmethod
    def get_full_info_by_name(self, city_name: str, forecast_count=7) -> CityInfoDTO:
        pass

    @abstractmethod
    def get_weather_info_by_name(self, city_name: str, forecast_count=7) -> CityWeatherDTO:
        pass

    @abstractmethod
    def get_or_create_country(self, city_name: str, country_code: str) -> CountryDTO:
        pass

    @abstractmethod
    def subscribe_city(self, user_id: int, city_name: str):
        pass

    @abstractmethod
    def get_user_cities_dict(self, user_id: int) -> dict[str, list[WeatherDTO]]:
        pass

    @abstractmethod
    def get_city_or_city_lsit_by_title(self, title: str) -> tuple[list[WeatherDTO], list[str]]:
        pass
