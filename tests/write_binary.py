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
    read_header, read_data, read_data_at, read_data_from_index, \
    search_data

from scripts.utils import bytes_to_str, str_to_bytes

f = open('genres.test.bin', 'rb')

#print(read_header(f))

def update_header(entity_file: BufferedReader, entity: EntityInfo):
    entity_file.seek(0)

    #entity_file.write()
    return

id, name = read_data_from_index(f, ENTITY['genres'], 1)
name = bytes_to_str(name)
print(id, name)

u = struct.pack(ENTITY['genres'].struct_format, id, str_to_bytes(name))
print(u)


f.close()