# type imports
from typing         import Final
from scripts.types  import \
    EntityInfo, CollectionType, MovieType, TitleType, \
    HeaderType, BlockHeaderType, BlockType

# module 'struct' pack and unpack formats
# string float char u16 u32 u64
#  {}s     f    B    H   I   Q  -> unsigned, {} is the length of the string
#               b    h   i   q  -> for signed
# '<' is for little endian format

#--------------------------------------------------------------------#
# all entitie files have a header with the quantity of items in them 
# and the size occupied in bytes for each item 
# num_items:u32, item_size:u16 -> 'IH'
HEADER: Final[EntityInfo] = EntityInfo( \
    name = 'header', \
    struct_size_format = 'IH', \
    classtype = HeaderType \
)

# controls the string size for each entity info
SIZE_GENRE: Final = 24
SIZE_COUNTRY: Final = 34
SIZE_COMPANY: Final = 35
SIZE_DECADE: Final = 6
SIZE_TITLE: Final = 80

# holds information about all entities files
ENTITY: Final[ dict[str, EntityInfo] ] = {
    'companies': EntityInfo( \
        name = 'companies', \
        struct_size_format = f'HI{SIZE_COMPANY}s', \
        classtype = CollectionType \
    ),
    'genres': EntityInfo( \
        name = 'genres', \
        struct_size_format = f'HI{SIZE_GENRE}s', \
        classtype = CollectionType \
    ),
    'countries': EntityInfo( \
        name = 'countries', \
        struct_size_format = f'HI{SIZE_COUNTRY}s', \
        classtype = CollectionType \
    ),
    'decades': EntityInfo( \
        name = 'decades', \
        struct_size_format = f'HI{SIZE_DECADE}s', \
        classtype = CollectionType \
    ),
    'titles': EntityInfo( \
        name = 'titles', \
        struct_size_format = f'II{SIZE_TITLE}s', \
        classtype = TitleType \
    ),
    'movies': EntityInfo( \
        name = 'movies', \
        struct_size_format = 'IIHff', \
        classtype = MovieType \
    )
}

#--------------------------------------------------------------------#
# all entities/relationships files based on blocks have a header with the quantity of blocks in them and the size occupied in bytes for each block
# num_blocks:u16, block_size:u32 -> 'HI'
HEADER_BLOCK: Final[EntityInfo] = EntityInfo( \
    name = 'headerblock', \
    struct_size_format = 'HI', \
    classtype = BlockHeaderType \
)

# information for the blocks in a blocks file
# BlockType.get_format()[1:] removes the '<' from the format
BLOCK: Final[EntityInfo] = EntityInfo( \
    name = 'block', \
    struct_size_format = \
        f'{BlockType.get_format()[1:]}{BlockType.get_data_size()}s', \
    classtype = BlockType \
)
