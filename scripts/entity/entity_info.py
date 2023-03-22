import struct

# string float char u16 u32 u64
#   Ns     f    B    H   I   Q  -> unsigned, N is the length of the string
#               b    h   i   q  -> for signed
# '<' is for little endian format

# all entitie files have a header with the quantity of items in them, the size occupied in bytes for each item and a offset to the end of the items in the file
# num_items:u32, item_size:u16, end_of_file:u64
header = '<IHQ'

class EntityInfo:
    def __init__(self, filename: str, struct_size_format: str, from_column: str, columns: list):
        self.filename = f'data/{filename}'
        self.struct_size = struct.calcsize(f'<{struct_size_format}')
        self.columns = columns
        self.from_column = from_column

ENTITY = {
    'companies': EntityInfo( \
        'companies.bin', \
        'H30s', \
        'production_companies', \
        ['id', 'name']
    ),
    'titles': EntityInfo( \
        'titles.bin', \
        'II150s', \
        'title', \
        ['id', 'movie_id', 'name']
    ),
    'genres': EntityInfo( \
        'genres.bin', \
        'H20s', \
        'genres', \
        ['id', 'name']
    ),
    'countries': EntityInfo( \
        'countries.bin', \
        'H20s', \
        'production_countries', \
        ['id', 'name']
    ),
    'movies': EntityInfo( \
        'movies.bin', \
        '', \
        '', \
        [] \
    )
}