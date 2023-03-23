#!/usr/bin/python

# configure module imports for user created modules outside the scope
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# importing types
from collections import namedtuple
from io import BufferedReader

import struct
from scripts.entity.entity_info \
    import EntityInfo, ENTITY, HEADER, EntityTuple, BaseTuple
from scripts.entity.io import \
    read_header, read_data, read_data_at, \
    search_data, search_by_id, cleanup_str

f = open('genres.test.bin', 'rb')

print(read_header(f))

genres = []
for e in read_data(f, ENTITY['genres']):
    # string must be cleaned up with:
    name = cleanup_str(e.name)

    genres.append(f'id: {e.id} - {name}')

print(genres)    

i = search_data(f, ENTITY['genres'], 3, search_by_id)
print(i)
print( read_data_at(f, ENTITY['genres'], i) )

f.close()

# block_size % item_size = items_per_block