from typing import NamedTuple

class SearchResultDTO(NamedTuple):
    name: str
    geo_id: int
    is_country: bool
    country_code: str
    country_name: str
