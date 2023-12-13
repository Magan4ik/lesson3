from abc import ABC, abstractmethod

import requests

from services import services_config
from services.service_interfaces import WikiInterface
from services.wiki.exceptions import *
from services.wiki.wiki_dto import WikiDTO, ImageDTO

class MediaWikiService(WikiInterface):
    @classmethod
    def get_info(cls, title: str, lang="en") -> WikiDTO:
        data = cls._get_data_from_api(title, lang=lang)
        cls._validate_data_or_raise(data)
        page = cls._get_page_if_valid(data)
        wiki_dto = cls._parse_page_to_dto(page)
        return wiki_dto

    @classmethod
    def get_info_by_id(cls, page_id: int, lang="en") -> WikiDTO:
        data = cls._get_data_from_api_by_id(page_id, lang=lang)
        cls._validate_data_or_raise(data)
        page = cls._get_page_if_valid(data)
        wiki_dto = cls._parse_page_to_dto(page)
        return wiki_dto

    @classmethod
    def _get_data_from_api(cls, city_name: str, lang="en") -> dict:
        api_url = f"https://{lang}.wikipedia.org/w/api.php"
        response = requests.get(api_url,
                                params={"action": "query", "format": "json",
                                        "prop": "extracts|pageimages", "exintro": True,
                                        "piprop": "original",
                                        "titles": city_name},
                                timeout=(cls.connect_timeout, cls.read_timeout)
                                )
        return response.json()

    @classmethod
    def _get_data_from_api_by_id(cls, page_id: int, lang="en") -> dict:
        api_url = f"https://{lang}.wikipedia.org/w/api.php"
        response = requests.get(api_url,
                                params={"action": "query", "format": "json",
                                        "prop": "extracts|pageimages", "exintro": True,
                                        "piprop": "original",
                                        "pageids": page_id},
                                timeout=(cls.connect_timeout, cls.read_timeout)
                                )
        return response.json()

    @staticmethod
    def _validate_data_or_raise(data: dict):
        # -- If not html or another --
        if not isinstance(data, dict):
            raise InvalidPesponceTypeError("the response is not in json format")

        # -- Errors in warnings.main --
        warnings = data.get("warnings")
        if warnings:
            errors = warnings.get("main")
            if errors:
                raise ExternalServerError(" & ".join(errors.values()))

    @staticmethod
    def _get_page_if_valid(data: dict):
        # -- ID no pages found == "-1" --
        page_id = next(iter(data["query"]["pages"]))  # get first page id
        page = data["query"]["pages"][page_id]
        if page_id == "-1":
            title = page["title"]
            raise PageNotFoundError(f'page {title} does not exist')

        if not page.get("original"):
            # Let's set default values instead of raise
            page["original"] = {"source": "",
                                "width": 0,
                                "height": 0}

        return page

    @staticmethod
    def _parse_page_to_dto(page: dict) -> WikiDTO:
        title = page['title']
        description = page['extract']
        image = ImageDTO(
            url=page["original"]["source"],
            width=page["original"]["width"],
            height=page["original"]["height"]
        )
        return WikiDTO(
            title=title,
            description=description,
            image=image
        )