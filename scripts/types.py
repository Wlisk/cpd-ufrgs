from typing import TypedDict

class MovieBaseDict(TypedDict):
    id: int
    title: str
    genres: list[str]
    companies: list[str]
    countries: list[str]
    release_year: int
    duration: float
    rating: float