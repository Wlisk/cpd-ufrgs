# type imports
from typing import Final
from scripts.types \
    import EntityInfo, CollectionType, MovieType, TitleType, \
    HeaderType, BlockHeaderType, BlockType

# string float char u16 u32 u64
#   Ns     f    B    H   I   Q  -> unsigned, N is the length of the string
#               b    h   i   q  -> for signed
# '<' is for little endian format


# all entitie files have a header with the quantity of items in them 
# and the size occupied in bytes for each item 
# num_items:u32, item_size:u16 -> 'IH'
HEADER: Final[EntityInfo] = EntityInfo( \
    name = 'header', \
    struct_size_format = 'IH', \
    classtype = HeaderType \
)

# holds information about all entities
ENTITY: Final[ dict[str, EntityInfo] ] = {
    'companies': EntityInfo( \
        name = 'companies', \
        struct_size_format = 'HI30s', \
        classtype = CollectionType \
    ),
    'titles': EntityInfo( \
        name = 'titles', \
        struct_size_format = 'II80s', \
        classtype = TitleType \
    ),
    'genres': EntityInfo( \
        name = 'genres', \
        struct_size_format = 'HI20s', \
        classtype = CollectionType \
    ),
    'countries': EntityInfo( \
        name = 'countries', \
        struct_size_format = 'HI30s', \
        classtype = CollectionType \
    ),
    'movies': EntityInfo( \
        name = 'movies', \
        struct_size_format = 'IIHff', \
        classtype = MovieType \
    ),
    'decades': EntityInfo( \
        name = 'decades', \
        struct_size_format = 'HIH', \
        classtype = CollectionType \
    )
}

# all entities/relationships files based on blocks have a header with the quantity of blocks in them and the size occupied in bytes for each block
# num_blocks:u16, block_size:u32 -> 'HI'
HEADER_BLOCK: Final[EntityInfo] = EntityInfo( \
    name = 'headerblock', \
    struct_size_format = 'HI', \
    classtype = BlockHeaderType \
)

# 
BLOCK: Final[EntityInfo] = EntityInfo( \
    name = 'block', \
    struct_size_format = \
        f'{BlockType.get_format()[1:]}{BlockType.get_data_size()}s', \
    classtype = BlockType \
)
