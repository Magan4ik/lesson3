from services.service_interfaces import CitySearchInterface
from services.weather.exceptions import CityNotFoundError
from services.weather.open_weather import WeatherTodayInterface, WeatherForecastInterface
from services.weather.weather_dto import WeatherDTO
from services.wiki.exceptions import PageNotFoundError
from services.wiki.media_wiki import WikiInterface
from weather.dtos import CityDTO, CityInfoDTO, CityWeatherDTO, CountryDTO

from typing import Type

from weather.repository_exceptions import CountryNotFound
from weather.repository_interfaces import CountryRepositoryInterface, CityRepositoryInterface


class CityInfoFacade:
    def __init__(self, weather_today_service: Type[WeatherTodayInterface],
                 weather_forecast_service: Type[WeatherForecastInterface],
                 wiki_service: Type[WikiInterface],
                 search_service: Type[CitySearchInterface],
                 country_repository: Type[CountryRepositoryInterface],
                 city_repository: Type[CityRepositoryInterface]):

        self.weather_today = weather_today_service
        self.weather_forecast = weather_forecast_service
        self.wiki = wiki_service
        self.search_service = search_service
        self.country_repository = country_repository
        self.city_repository = city_repository

    def get_full_info_by_name(self, city_name: str, country_code: str = None, forecast_count: int = 7, commit: bool = True) -> CityInfoDTO:
        if country_code:
            title = f"{city_name},{country_code}"
        else:
            title = city_name

        city_weather_dto = self.get_weather_info_by_name(city_name=title, forecast_count=forecast_count)
        city = self.city_repository.get_city_by_name(name=city_weather_dto.name)
        if not city:
            try:
                wiki_dto = self.wiki.get_info(title=city_name)
                wiki_page = wiki_dto.description
                image = wiki_dto.image.url
            except PageNotFoundError:
                wiki_page = ""
                image = ""

        else:
            wiki_page = city.wiki_page
            image = city.image

        city_dto = CityInfoDTO(
            name=city_name,
            lat=city_weather_dto.lat,
            lon=city_weather_dto.lon,
            country_code=city_weather_dto.country_code,
            weather_now=city_weather_dto.weather_now,
            weather_forecast=city_weather_dto.weather_forecast,
            wiki_page=wiki_page,
            image=image
        )

        if commit and not city:
            self.get_or_create_country(city_name=city_dto.name, country_code=city_dto.country_code)
            self.city_repository.create_city(city_dto=city_dto)

        return city_dto

    def get_weather_info_by_name(self, city_name: str, forecast_count=7) -> CityWeatherDTO:
        weather_today_dto = self.weather_today.get_weather(city=city_name)
        weather_forecast_dtos = self.weather_forecast.get_weather(city=city_name, cnt=forecast_count)
        return CityWeatherDTO(
            name=weather_today_dto.city.name,
            lat=weather_today_dto.city.coordinates.lat,
            lon=weather_today_dto.city.coordinates.lon,
            country_code=weather_today_dto.city.country_code,
            weather_now=weather_today_dto,
            weather_forecast=weather_forecast_dtos
        )

    def get_or_create_country(self, city_name: str, country_code: str) -> CountryDTO:
        country = self.country_repository.get_country_by_code(code=country_code)
        if not country:
            search_result = self.search_service.search(name=city_name)
            country = CountryDTO(
                name=search_result.country_name,
                code=search_result.country_code
            )
            self.country_repository.create_country(country_dto=country)
        return country

    def subscribe_city(self, user_id: int, city_name: str):
        self.city_repository.subscribe_user(user_id=user_id, city_name=city_name)

    def get_user_cities_dict(self, user_id: int) -> dict[str, list[WeatherDTO]]:
        cities = self.city_repository.get_city_list_by_user_id(user_id=user_id)
        weather_cities_dict = dict()

        for city in cities:
            weather_dto = self.weather_today.get_weather(city=city.name)
            if city.country.name not in weather_cities_dict.keys():
                weather_cities_dict[city.country.name] = [weather_dto]
            else:
                weather_cities_dict[city.country.name].append(weather_dto)

        return weather_cities_dict

    def get_city_or_city_lsit_by_title(self, title: str) -> tuple[list[WeatherDTO], list[str]]:
        search_result = self.search_service.search(name=title)
        cities = list()
        not_found_cities = list()
        if not search_result.is_country:
            try:
                weather_dto = self.weather_today.get_weather(city=f"{search_result.name},{search_result.country_code}")
                cities.append(weather_dto)
            except CityNotFoundError:
                not_found_cities.append(search_result.name)
            return cities, not_found_cities

        cities_of_country = self.search_service.search_childrens(geo_id=search_result.geo_id)
        for city in cities_of_country:
            try:
                weather_dto = self.weather_today.get_weather(city=f"{city.name},{city.country_code}")
                cities.append(weather_dto)
            except CityNotFoundError:
                not_found_cities.append(city.name)

        return cities, not_found_cities

