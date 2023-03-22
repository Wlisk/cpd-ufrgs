import struct
from collections import namedtuple
from scripts.entity.entity_info import EntityInfo, ENTITY

f = open('genres.bin', 'rb')

struct_size = ENTITY['genres'].struct_size
Genre = ENTITY['genres'].namedtuple
genres = {}

header = EntityInfo( \
    'header', \
    'IHQ', \
    '', \
    ['num_items', 'item_size', 'end_of_file'] \
)

def read_entity_header(entity_file) -> namedtuple: 
    # guarantees that it's at the init of the file
    entity_file.seek(0)
    # read the header structure data
    header_data = entity_file.read(header.struct_size)
    # generate and return a namedtuple with the data readed within
    return header.namedtuple._make( \
        struct.unpack(header.struct_format, header_data) \
    )

print(read_entity_header(f))


def t():
    while row := f.read(struct_size):

        # < is for little-endian architecture configuration
        # H is for unsigned short (2 bytes)
        # 18s is for char[18] (18 bytes)

        # if end of file or cannot read offset bytes further then exit loop
        # as there is no more genres to read
        if len(row) < struct_size: break
        
        genre = Genre._make( struct.unpack('<H20s', row) )

        # if id is equal 0, it means there is no more valid genres to read
        if genre.id == 0: break

        genres[genre.id] = str(genre.name, 'UTF-8').replace('\x00','')

f.close()

#print(genres)

# block_size % item_size = items_per_block