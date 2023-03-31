# type imports
from typing import TypedDict, NamedTuple

from dataclasses import dataclass
from collections import namedtuple
from struct import calcsize

#--------------------------------------------------------------------#
# type to extracted data from csv
class MovieBaseDict(TypedDict):
    id: int
    title: str
    genres: list[str]
    companies: list[str]
    countries: list[str]
    release_year: int
    duration: float
    rating: float

#--------------------------------------------------------------------#
# base entity
@dataclass
class CollectionType:
    id: int             # id of the item
    name: str           # the item data
    
    def make(data: tuple):
        if len(data) < 2: return None
        return CollectionType(*data)


#--------------------------------------------------------------------#
# title entity  
@dataclass
class TitleType:
    id: int             # title id
    movie_id: int       # movie id, so we can get a movie info by title
    name: str           # the title

    def make(data: tuple):
        if len(data) < 3: return None
        return TitleType(*data)

#--------------------------------------------------------------------#
# header of all entities
@dataclass
class HeaderType:
    num_items: int      # u32, number of items in an entity file 
    item_size: int      # u16, size of the item structure in the entity file
    end_of_file: int    # u64, offset to the end of the last item

    def make(data: tuple):
        if len(data) < 3: return None
        return HeaderType(*data)

#--------------------------------------------------------------------#
# movie entity
@dataclass
class MovieType:
    id: int             # movie id
    title_id: int       # title id
    release_year: int   # year it was released
    duration: float     # duration of the movie in minutes
    rating: float       # votes rating between 0.0 and 10.0

    def make(data: tuple):
        if len(data) < 5: return None
        return MovieType(*data)

#--------------------------------------------------------------------#
# alias to incompass all created namedtuple types
BaseType = CollectionType | TitleType | MovieType
AllType = BaseType | HeaderType

#--------------------------------------------------------------------#
# object to hold information about an entity
class EntityInfo:
    def __init__(self, name: str, struct_size_format: str, classtype: AllType):
        self.name = name
        self.filename = f'{name}.bin'
        self.struct_format = f'<{struct_size_format}'
        self.struct_size = calcsize(self.struct_format)
        self.classtype = classtype
        