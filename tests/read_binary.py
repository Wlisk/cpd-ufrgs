#!/usr/bin/python

# configure module imports for user created modules outside the scope
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# importing types
from collections import namedtuple
from io import BufferedReader

import struct
from scripts.entity.entity_info import EntityInfo, ENTITY, HEADER

f = open('genres.test.bin', 'rb')

struct_size = ENTITY['genres'].struct_size
Genre = ENTITY['genres'].namedtuple
genres = {}

def read_entity_header(entity_file: BufferedReader) -> namedtuple: 
    # guarantees that it's at the init of the file
    entity_file.seek(0)
    # read the header structure data
    header_data = entity_file.read(HEADER.struct_size)
    # generate and return a namedtuple with the data readed within
    return HEADER.namedtuple._make( \
        struct.unpack(HEADER.struct_format, header_data) \
    )

print(read_entity_header(f))

def read_entity_data(entity_file: BufferedReader, entity: EntityInfo) -> namedtuple:
    # points to the first byte after the header structure
    entity_file.seek(HEADER.struct_size)

    while e := entity_file.read(entity.struct_size):
        # if end of file or cannot read offset bytes further then exit loop
        # as there is no more entity data to read
        if len(e) < entity.struct_size: break

        data = entity.namedtuple._make( \
            struct.unpack(entity.struct_format, e) \
        )

        if data.id == 0: break

        yield data

for e in read_entity_data(f, ENTITY['genres']):
    print(e)


def t():
    while row := f.read(struct_size):

        # < is for little-endian architecture configuration
        # H is for unsigned short (2 bytes)
        # 18s is for char[18] (18 bytes)

        # if end of file or cannot read offset bytes further then exit loop
        # as there is no more entity data to read
        if len(row) < struct_size: break
        
        genre = Genre._make( struct.unpack('<H20s', row) )

        # if id is equal 0, it means there is no more valid genres to read
        if genre.id == 0: break

        genres[genre.id] = str(genre.name, 'UTF-8').replace('\x00','')

f.close()

#print(genres)

# block_size % item_size = items_per_block