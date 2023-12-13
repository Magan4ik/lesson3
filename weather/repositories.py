from typing import Optional

from django.contrib.auth import get_user_model

from weather.dtos import CountryDTO, CityDTO, CityInfoDTO
from weather.models import City, Country
from weather.repository_exceptions import CountryNotFound
from weather.repository_interfaces import CountryRepositoryInterface, CityRepositoryInterface

User = get_user_model()

class CountryDjangoORMRepository(CountryRepositoryInterface):

    @classmethod
    def get_country_by_code(cls, code: str) -> Optional[CountryDTO]:
        country = Country.objects.filter(country_code=code).first()
        if not country:
            return None

        return cls._map_model_to_dto(country)

    @classmethod
    def _map_model_to_dto(cls, country: Country) -> CountryDTO:
        return CountryDTO(
            name=country.country_name,
            code=country.country_code
        )

    @staticmethod
    def create_country(country_dto: CountryDTO) -> None:
        Country.objects.create(country_name=country_dto.name, country_code=country_dto.code)

    @staticmethod
    def subscribe_user(user_id: int, country_code: str):
        user = User.objects.filter(pk=user_id).first()
        country = Country.objects.filter(country_code=country_code).first()
        if user in country.users.all():
            country.users.remove(user)
        else:
            country.users.add(user)


class CityDjangoORMRepository(CityRepositoryInterface):

    @classmethod
    def get_city_by_name(cls, name: str) -> Optional[CityDTO]:
        city = City.objects.filter(city_name=name).first()
        if not city:
            return None
        return cls._map_model_to_dto(city)

    @classmethod
    def _map_model_to_dto(cls, city: City) -> CityDTO:
        country = CountryDTO(
            name=city.city_country.country_name,
            code=city.city_country.country_code
        )
        return CityDTO(
            id=city.pk,
            name=city.city_name,
            lat=city.lat,
            lon=city.lon,
            country=country,
            wiki_page=city.wiki_page,
            image=city.image_url
        )

    @classmethod
    def create_city(cls, city_dto: CityInfoDTO) -> CityDTO:
        country = Country.objects.filter(country_code=city_dto.country_code).first()
        if not country:
            raise CountryNotFound(f"Unpossible to get country with this code: {city_dto.country_code}")
        city = City.objects.create(
            city_name=city_dto.name,
            lat=city_dto.lat,
            lon=city_dto.lon,
            city_country=country,
            wiki_page=city_dto.wiki_page,
            image_url=city_dto.image
        )
        country.cities.add(city)
        return cls._map_model_to_dto(city=city)

    @staticmethod
    def subscribe_user(user_id: int, city_name: str):
        user = User.objects.filter(pk=user_id).first()
        city = City.objects.filter(city_name=city_name).first()
        if user in city.users.all():
            city.users.remove(user)
        else:
            city.users.add(user)

    @classmethod
    def get_city_list_by_user_id(cls, user_id: int) -> list[CityDTO]:
        user = User.objects.filter(pk=user_id).first()
        cities = user.cities.all()
        city_list = list()
        for city in cities:
            city_list.append(cls._map_model_to_dto(city=city))

        return city_list
