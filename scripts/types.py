# type imports
from typing import TypedDict

from dataclasses import dataclass, astuple
from struct import calcsize
from scripts.utils import str_to_bytes, bytes_to_str
from scripts.config import BLOCK_SIGNATURE, BLOCK_SIZE

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
    block_pos: int      # position of the block in a block oriented file
    name: str|bytes     # the item data
    #
    @staticmethod
    def make(data: tuple):
        if len(data) < 3: return None
        return CollectionType(*data)
    #
    def to_bytestuple(self) -> tuple:
        c = CollectionType.make(\
            (self.id, self.block_pos, str_to_bytes(self.name)) \
        )
        return astuple(c)
    #
    def normalize(self):
        if type(self.name) == bytes:
            self.name = bytes_to_str(self.name)
        return self

#--------------------------------------------------------------------#
# title entity  
@dataclass
class TitleType:
    id: int             # title id
    movie_id: int       # movie id, so we can get a movie info by title
    name: str|bytes     # the title

    @staticmethod
    def make(data: tuple):
        if len(data) < 3: return None
        return TitleType(*data)
    
    def to_bytestuple(self) -> tuple:
        t = TitleType.make((self.id, self.movie_id, str_to_bytes(self.name)))
        return astuple(t)
    
    def normalize(self):
        if type(self.name) == bytes:
            self.name = bytes_to_str(self.name)
        return self

#--------------------------------------------------------------------#
# header of all entities
@dataclass
class HeaderType:
    num_items: int      # u32, number of items in an entity file 
    item_size: int      # u16, size of the item structure in the entity file

    @staticmethod
    def make(data: tuple):
        if len(data) < 2: return None
        return HeaderType(*data)
    
    def to_bytestuple(self) -> tuple:
        return astuple(self)

#--------------------------------------------------------------------#
# movie entity
@dataclass
class MovieType:
    id: int             # movie id
    title_pos: int      # poition of the title in the file (title "pointer")
    release_year: int   # year it was released
    duration: float     # duration of the movie in minutes
    rating: float       # votes rating between 0.0 and 10.0

    @staticmethod
    def make(data: tuple):
        if len(data) < 5: return None
        return MovieType(*data)
    
    def to_bytestuple(self) -> tuple:
        return astuple(self)

#--------------------------------------------------------------------#
# block of a entity/relationship based on blocks
@dataclass
class BlockType:
    block_signature: int
    block_id: int
    end_data: int
    data: bytes

    def __init__(self, block_id: int, end_data: int, data: bytes):
        self.block_id = block_id
        self.end_data = end_data
        self.data = data
        self.block_signature = BLOCK_SIGNATURE

    @staticmethod
    def make(data: tuple):
        if len(data) < 3: return None
        return BlockType(*data)
    
    @staticmethod
    def create(block_id: int):
        return BlockType(\
            block_id, \
            calcsize(BlockType.get_format()), \
            BlockType.get_data_size() * b'0' \
        )
    
    def to_bytestuple(self) -> tuple:
        return astuple(self)
    
    @staticmethod
    def get_format():
        return 'IHI' #u32, u16, u32
    
    @staticmethod
    def get_data_size():
        return BLOCK_SIZE - calcsize(BlockType.get_format())

#--------------------------------------------------------------------#
# header of all entities/relationships based on blocks
@dataclass
class BlockHeaderType:
    num_blocks: int
    block_size: int = BLOCK_SIZE

    def __init__(self, num_blocks: int):
        self.num_blocks = num_blocks

    @staticmethod
    def make(data: tuple):
        if len(data) < 1: return None
        return BlockHeaderType(*data)
    
    def to_bytestuple(self) -> tuple:
        return astuple(self)

#--------------------------------------------------------------------#
# alias to incompass all created namedtuple types
BaseType = CollectionType | TitleType | MovieType
AllHeaderType = HeaderType | BlockHeaderType 
AllType = BaseType | AllHeaderType

#--------------------------------------------------------------------#
# object to hold information about an entity
class EntityInfo:
    def __init__(self, name: str, struct_size_format: str, classtype: AllType):
        self.name = name
        self.struct_format = f'<{struct_size_format}'
        self.struct_size = calcsize(self.struct_format)
        self.classtype = classtype
        



