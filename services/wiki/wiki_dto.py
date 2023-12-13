from typing import NamedTuple

class ImageDTO(NamedTuple):
    url: str
    width: int
    height: int

class WikiDTO(NamedTuple):
    title: str
    description: str
    image: ImageDTO
