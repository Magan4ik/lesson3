from abc import ABCMeta, abstractmethod

import requests
from requests import Response

from services.maps.exceptions import GoogleMapsApiError
from services.service_interfaces import MapsImageInterface
from services.services_config import get_google_maps_key


class GoogleMapsService(MapsImageInterface):
    _api_key = get_google_maps_key()

    @classmethod
    def get_image_url(cls, center: str, zoom=9, size='400x300') -> str:
        response = cls._get_response_from_api(center=center)
        return cls._get_url_or_raise(response)

    @classmethod
    def _get_response_from_api(cls, center: str, zoom=9, size='400x300') -> Response:
        res = requests.get(url="https://maps.googleapis.com/maps/api/staticmap",
                           params={"center": center, "zoom": zoom, "size": size,
                                   "key": cls._api_key}
                           )
        return res

    @classmethod
    def _get_url_or_raise(cls, res: Response) -> str:
        if res:
            if res.status_code == 200:
                return res.request.url
        raise GoogleMapsApiError("status code:", res.status_code)


