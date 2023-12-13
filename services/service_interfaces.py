from abc import ABCMeta, abstractmethod

from services.citites.cities_dto import SearchResultDTO
from services import services_config
from services.weather.weather_dto import WeatherDTO
from services.wiki.wiki_dto import WikiDTO


class CitySearchInterface(metaclass=ABCMeta):
    connect_timeout = services_config.settings["CONNECT_TIMEOUT"]
    read_timeout = services_config.settings["READ_TIMEOUT"]

    @classmethod
    @abstractmethod
    def search(cls, name: str) -> SearchResultDTO:
        pass

    @classmethod
    @abstractmethod
    def search_childrens(cls, geo_id: int) -> list[SearchResultDTO]:
        pass


class MapsImageInterface(metaclass=ABCMeta):

    @abstractmethod
    def get_image_url(self, center: str):
        pass

class WeatherTodayInterface(metaclass=ABCMeta):
    connect_timeout = services_config.settings["CONNECT_TIMEOUT"]
    read_timeout = services_config.settings["READ_TIMEOUT"]

    @classmethod
    @abstractmethod
    def get_weather(cls, city: str) -> WeatherDTO:
        pass


class WeatherForecastInterface(metaclass=ABCMeta):
    connect_timeout = services_config.settings["CONNECT_TIMEOUT"]
    read_timeout = services_config.settings["READ_TIMEOUT"]

    @classmethod
    @abstractmethod
    def get_weather(cls, city: str, cnt: int = 7) -> list[WeatherDTO]:
        pass

class WikiInterface(metaclass=ABCMeta):
    connect_timeout = services_config.settings["CONNECT_TIMEOUT"]
    read_timeout = services_config.settings["READ_TIMEOUT"]

    @classmethod
    @abstractmethod
    def get_info(cls, title: str) -> WikiDTO:
        pass

