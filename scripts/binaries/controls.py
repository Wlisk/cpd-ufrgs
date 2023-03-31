# type imports
from scripts.types \
    import EntityInfo, HeaderType, CollectionType, MovieType, TitleType

# string float char u16 u32 u64
#   Ns     f    B    H   I   Q  -> unsigned, N is the length of the string
#               b    h   i   q  -> for signed
# '<' is for little endian format


# all entitie files have a header with the quantity of items in them, the size occupied in bytes for each item and a offset to the end of the items in the file
# num_items:u32, item_size:u16, end_of_file:u64 -> 'IHQ'
HEADER = EntityInfo( \
    name = 'header', \
    struct_size_format = 'IHQ', \
    classtype = HeaderType \
)

# holds information about all entities
ENTITY: dict[str, EntityInfo] = {
    'companies': EntityInfo( \
        name = 'companies', \
        struct_size_format = 'H30s', \
        classtype = CollectionType
    ),
    'titles': EntityInfo( \
        name = 'titles', \
        struct_size_format = 'II80s', \
        classtype = TitleType
    ),
    'genres': EntityInfo( \
        name = 'genres', \
        struct_size_format = 'H20s', \
        classtype = CollectionType
    ),
    'countries': EntityInfo( \
        name = 'countries', \
        struct_size_format = 'H30s', \
        classtype = CollectionType
    ),
    'movies': EntityInfo( \
        name = 'movies', \
        struct_size_format = 'II', \
        classtype = MovieType \
    )
}