from abc import ABCMeta, abstractmethod
from typing import Optional

from weather.dtos import CountryDTO, CityDTO, CityInfoDTO


class CountryRepositoryInterface(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_country_by_code(cls, code: str) -> Optional[CountryDTO]:
        pass

    @staticmethod
    @abstractmethod
    def create_country(country_dto: CountryDTO) -> None:
        pass

    @staticmethod
    @abstractmethod
    def subscribe_user(user_id: int, country_code: str):
        pass


class CityRepositoryInterface(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_city_by_name(cls, name: str) -> Optional[CityDTO]:
        pass

    @classmethod
    @abstractmethod
    def create_city(cls, city_dto: CityInfoDTO) -> CityDTO:
        pass

    @staticmethod
    @abstractmethod
    def subscribe_user(user_id: int, city_name: str):
        pass

    @classmethod
    @abstractmethod
    def get_city_list_by_user_id(cls, user_id: int) -> list[CityDTO]:
        pass
