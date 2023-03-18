import struct
from collections import namedtuple
import codecs

f = open('genres.bin', 'rb')
offset = 20

Genre = namedtuple('Genre', ['id', 'name'])
genres = {}

while row := f.read(offset):

    # < is for little-endian architecture configuration
    # H is for unsigned short (2 bytes)
    # 18s is for char[18] (18 bytes)

    # if end of file or cannot read offset bytes further then exit loop
    # as there is no more genres to read
    if len(row) < offset: break
    
    #print( struct.unpack('<H18s', row) )
    genre = Genre._make( struct.unpack('<H18s', row) )

    # if id is equal 0, it means there is no more valid genres to read
    if genre.id == 0: break

    genres[genre.id] = str(genre.name, 'UTF-8').replace('\x00','')

f.close()

print(genres)