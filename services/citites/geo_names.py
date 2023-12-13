import requests

from services.citites.cities_dto import SearchResultDTO
from services.service_interfaces import CitySearchInterface
from services.services_config import get_geonames_username, settings
from services.citites.exceptions import *


# GeoNames API: https://www.geonames.org/export/ws-overview.html

class GeoNamesSearchService(CitySearchInterface):
    username = get_geonames_username()

    @classmethod
    def search(cls, name: str) -> SearchResultDTO:
        data = cls._get_json_from_api_by_name(name)
        cls._validate_data_or_raise(data)
        return cls._parse_data_to_dto(data)

    @classmethod
    def search_childrens(cls, geo_id: int) -> list[SearchResultDTO]:
        """Returns the children (admin divisions and populated places) for a given geonameId"""
        data = cls._get_json_from_api_by_id(geo_id=geo_id)
        cls._validate_data_or_raise(data=data)
        city_list = cls._parse_data_to_city_list(data=data)
        return city_list

    @classmethod
    def _get_json_from_api_by_name(cls, name: str) -> dict:
        res = requests.get("http://api.geonames.org/searchJSON",
                           params={"q": name, "username": cls.username},
                           timeout=(cls.connect_timeout, cls.read_timeout))
        return res.json()

    @classmethod
    def _get_json_from_api_by_id(cls, geo_id: int) -> dict:
        res = requests.get("http://api.geonames.org/childrenJSON?",
                           params={"geonameId": geo_id, "username": cls.username},
                           timeout=(cls.connect_timeout, cls.read_timeout))
        return res.json()

    @staticmethod
    def _validate_data_or_raise(data: dict):
        if data.get("status"):
            mes = data["status"]["message"]
            code = data["status"]["value"]
            raise ExternalServerError(f"GeoNames Error with code {code}: {mes}")

        if len(data["geonames"]) == 0:
            raise CityOrCountryNotFound("Empty GeoNames list was returned")

    @classmethod
    def _parse_data_to_city_list(cls, data: dict) -> list[SearchResultDTO]:
        city_list = list()
        for index in range(len(data["geonames"])):
            search_dto = cls._parse_data_to_dto(data, index=index)
            city_list.append(search_dto)

        return city_list

    @staticmethod
    def _parse_data_to_dto(data: dict, index=0) -> SearchResultDTO:
        geoid = data["geonames"][index]["geonameId"]
        name = data["geonames"][index]["name"]

        # У стран в поле 'name' такое же значение как и в 'countryName'
        is_country = data["geonames"][index].get("countryName", "") == data["geonames"][index]["name"]

        return SearchResultDTO(
            name=name,
            geo_id=geoid,
            is_country=is_country,
            country_code=data["geonames"][index].get("countryCode", ""),
            country_name=data["geonames"][index].get("countryName", "")
        )
