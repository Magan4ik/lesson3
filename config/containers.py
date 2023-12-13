from dependency_injector import containers, providers

from services.citites.geo_names import GeoNamesSearchService
from services.service_interfaces import WikiInterface, CitySearchInterface, WeatherTodayInterface, \
    WeatherForecastInterface
from services.weather.open_weather import OpenWeatherTodayService, OpenWeatherForecastService
from services.wiki.media_wiki import MediaWikiService
from weather.facade_interfaces import CityInfoFacadeInterface
from weather.facades import CityInfoFacade
from weather.repositories import CountryDjangoORMRepository, CityDjangoORMRepository
from weather.repository_interfaces import CountryRepositoryInterface, CityRepositoryInterface


class RepositoryContainer(containers.DeclarativeContainer):
    country_repository: providers.Provider[CountryRepositoryInterface] = providers.Factory(
        CountryDjangoORMRepository
    )
    city_repository: providers.Provider[CityRepositoryInterface] = providers.Factory(
        CityDjangoORMRepository
    )

class ServiceContainer(containers.DeclarativeContainer):
    wiki_service: providers.Provider[WikiInterface] = providers.Factory(MediaWikiService)
    search_service: providers.Provider[CitySearchInterface] = providers.Factory(
        GeoNamesSearchService
    )
    weather_today_service: providers.Provider[WeatherTodayInterface] = providers.Factory(
        OpenWeatherTodayService
    )
    weather_forecast_service: providers.Provider[WeatherForecastInterface] = providers.Factory(
        OpenWeatherForecastService
    )


class FacadeContainer(containers.DeclarativeContainer):
    city_info_facade: providers.Provider[CityInfoFacadeInterface] = providers.Factory(
        CityInfoFacade,
        weather_today_service=ServiceContainer.weather_today_service,
        weather_forecast_service=ServiceContainer.weather_forecast_service,
        wiki_service=ServiceContainer.wiki_service,
        search_service=ServiceContainer.search_service,
        country_repository=RepositoryContainer.country_repository,
        city_repository=RepositoryContainer.city_repository
    )
