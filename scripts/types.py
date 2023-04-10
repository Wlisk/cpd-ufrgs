# type imports
from typing         import TypedDict
# module imports 
from dataclasses    import dataclass, astuple
from struct         import calcsize
from scripts.utils  import str_to_bytes, bytes_to_str
# const imports
from scripts.config import BLOCK_SIGNATURE, BLOCK_SIZE

#--------------------------------------------------------------------#
# type to extracted data from csv
class MovieBaseDict(TypedDict):
    id: int
    title: str
    genres: list[str]
    companies: list[str]
    countries: list[str]
    release_year: str
    duration: float
    rating: float

#--------------------------------------------------------------------#
# base type for all other types
class BaseType:
    def normalize(self): return self

    # convert this object data into a tuple so it can be packed 
    # CAUTION: this function only works for @dataclass instances
    def to_bytestuple(self) -> tuple: return astuple(self)

#--------------------------------------------------------------------#
# base entity, for entities that hold a collection of data (N-to-N or 1-to-N)
@dataclass
class CollectionType(BaseType):
    id: int             # id of the item
    block_pos: int      # position of the block in a block oriented file
    name: str|bytes|bytearray     # the item data
        
    # convert this object data into a tuple so it can be packed 
    def to_bytestuple(self) -> tuple:
        if type(self.name) == str: 
            self.name = str_to_bytes(self.name)
        return astuple( self )
    
    # if the name is in a bytes like format 'normalize' it to string format
    def normalize(self) -> 'CollectionType':
        if type(self.name) != str:
            self.name = bytes_to_str(self.name)
        return self
    
    # create a new instance of this type with the tuple passed (3 args)
    @staticmethod
    def make(data: tuple) -> 'CollectionType': return CollectionType(*data)

#--------------------------------------------------------------------#
# title entity  
@dataclass
class TitleType(BaseType):
    id: int             # title id
    movie_id: int       # movie id, so we can get a movie info by title
    name: str|bytes|bytearray     # the title
    
    # convert this object data into a tuple so it can be packed 
    def to_bytestuple(self) -> tuple:
        if type(self.name) == str: 
            self.name = str_to_bytes(self.name)
        return astuple( self )
    
    # if the name is in a bytes like format 'normalize' it to string format
    def normalize(self):
        if type(self.name) != str: 
            self.name = bytes_to_str(self.name)
        return self
    
    # create a new instance of this type with the tuple passed (3 args)
    @staticmethod
    def make(data: tuple) -> 'TitleType': return TitleType(*data)

#--------------------------------------------------------------------#
# all entities header
@dataclass
class HeaderType(BaseType):
    num_items: int      # u32, number of items in an entity file 
    item_size: int      # u16, size of the item structure in the entity file
    
    # create a new instance of this type with the tuple passed (2 args)
    @staticmethod
    def make(data: tuple) -> 'HeaderType': return HeaderType(*data)

#--------------------------------------------------------------------#
# movie entity
@dataclass
class MovieType(BaseType):
    id: int             # movie id
    title_pos: int      # poition of the title in the file (title "pointer")
    release_year: int   # year it was released
    duration: float     # duration of the movie in minutes
    rating: float       # votes rating between 0.0 and 10.0

    # create a new instance of this type with the tuple passed 5 args)
    @staticmethod
    def make(data: tuple) -> 'MovieType': return MovieType(*data)

#--------------------------------------------------------------------#
# block of a entity/relationship based on blocks
@dataclass
class BlockType(BaseType):
    block_signature: int
    block_id: int
    num_items: int
    end_data: int
    data: bytes|bytearray = b''

    # create a new instance of this type with the tuple passed (5 args)
    @staticmethod
    def make(data: tuple): return BlockType(*data)

    # returns the string of the struct format of a block in a block file
    # excluding the format for the data part
    @staticmethod
    def get_format(): return '<iHII' #i32, u16, u32, u32
    
    # gets the max data size for a block in a block file
    @staticmethod
    def get_data_size():
        return BLOCK_SIZE - calcsize(BlockType.get_format())
    
    # create a block a new block for disk write 
    # with default values and a given ID
    @staticmethod
    def create(block_id: int):
        return BlockType(\
            BLOCK_SIGNATURE, block_id, 0, 0, \
            BlockType.get_data_size() * b'0' \
        )

    # create a new block with default values and a given ID
    @staticmethod
    def new(block_id: int):
        return BlockType(BLOCK_SIGNATURE, block_id, 0, 0, b'0')

#--------------------------------------------------------------------#
# header of all entities/relationships based on blocks
@dataclass
class BlockHeaderType(BaseType):
    num_blocks: int
    block_size: int = BLOCK_SIZE

    # create a new instance of this type with the tuple passed (1 args)
    @staticmethod
    def make(data: tuple) -> 'BlockHeaderType': return BlockHeaderType(*data)
    
#--------------------------------------------------------------------#
# alias to incompass all created types
AllEType = CollectionType | TitleType | MovieType
AllHType = HeaderType | BlockHeaderType 
AllType = AllEType | AllHType

#--------------------------------------------------------------------#
# object to hold information about an entity
class EntityInfo:
    name: str               # the entity name (also name of the file)
    struct_format: str      # format (struct) of each item
    struct_size: int        # size of the struct of each item
    classtype: AllType      # wich class the entity is 

    def __init__(self, name: str, struct_size_format: str, classtype: AllType):
        self.name           = name
        self.struct_format  = f'<{struct_size_format}'
        self.struct_size    = calcsize(self.struct_format)
        self.classtype      = classtype
        



