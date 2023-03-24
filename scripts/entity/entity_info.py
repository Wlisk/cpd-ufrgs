import struct
from collections import namedtuple
from typing import NamedTuple

# string float char u16 u32 u64
#   Ns     f    B    H   I   Q  -> unsigned, N is the length of the string
#               b    h   i   q  -> for signed
# '<' is for little endian format

# all entitie files have a header with the quantity of items in them, the size occupied in bytes for each item and a offset to the end of the items in the file
# num_items:u32, item_size:u16, end_of_file:u64 = 'IHQ'

# object to hold information about an entity
class EntityInfo:
    def __init__(self, name: str, struct_size_format: str, from_column: str, columns: list):
        self.name = name
        self.filename = f'data/{name}.bin'
        self.struct_size = struct.calcsize(f'<{struct_size_format}')
        self.from_column = from_column
        self.namedtuple = namedtuple(name.capitalize(), columns)
        self.struct_format = f'<{struct_size_format}'

# types to give intelisense with namedtuple
class EntityTuple(NamedTuple):
    id: int
    name: str
class TitleTuple(EntityTuple):
    movie_id: int
class MovieTuple(NamedTuple):
    id: int
    title_id: int
class HeaderTuple(NamedTuple):
    num_items: int
    item_size: int
    end_of_file: int
# alias to incompass all created namedtuple types
BaseTuple = EntityTuple | TitleTuple | MovieTuple

HEADER = EntityInfo( \
    'header', \
    'IHQ', \
    '', \
    ['num_items', 'item_size', 'end_of_file'] \
)

ENTITY = {
    'companies': EntityInfo( \
        'companies', \
        'H30s', \
        'production_companies', \
        ['id', 'name']
    ),
    'titles': EntityInfo( \
        'titles', \
        'II150s', \
        'title', \
        ['id', 'movie_id', 'name']
    ),
    'genres': EntityInfo( \
        'genres', \
        'H20s', \
        'genres', \
        ['id', 'name']
    ),
    'countries': EntityInfo( \
        'countries', \
        'H20s', \
        'production_countries', \
        ['id', 'name']
    ),
    'movies': EntityInfo( \
        'movies', \
        'II', \
        '', \
        ['id', 'title_id'] \
    )
}