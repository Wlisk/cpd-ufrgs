import struct
from collections import namedtuple
from scripts.entity.entity_info import EntityInfo

f = open('genres.bin', 'rb')
offset = 20

Genre = namedtuple('Genre', ['id', 'name'])
genres = {}

header_format = '<IHQ'

def read_entity_header(entity_file):
    # guarantees that is at the init of the file
    entity_file.seek(0)

    HEADER = namedtuple('Header', ['num_items', 'item_size', 'end_of_file'])

    header_size = struct.calcsize(header_format)

    header_data = entity_file.read(header_size)

    return HEADER._make( struct.unpack(header_format, header_data) )




while row := f.read(offset):

    # < is for little-endian architecture configuration
    # H is for unsigned short (2 bytes)
    # 18s is for char[18] (18 bytes)

    # if end of file or cannot read offset bytes further then exit loop
    # as there is no more genres to read
    if len(row) < offset: break
    
    genre = Genre._make( struct.unpack('<H20s', row) )

    # if id is equal 0, it means there is no more valid genres to read
    if genre.id == 0: break

    genres[genre.id] = str(genre.name, 'UTF-8').replace('\x00','')

f.close()

print(genres)

# block_size % item_size = items_per_block