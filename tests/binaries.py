#!/usr/bin/python

# configure module imports for user created modules outside the scope
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.io.serial import Serial
from scripts.types import CollectionType

def t1():
    genres_stream = Serial('genres')
    genres_stream.open()

    newdata: list[CollectionType] = []

    newdata.append( CollectionType(1, 0, "Richard") )
    newdata.append( CollectionType(2, 32, "Rasputin") )

    genres_stream.write_all(newdata)
    pos = genres_stream._file.seek(0, 2) # 2 - SEEK_END
    print(pos)

    genres_stream.write( CollectionType(3, 80,  "Anneliz") )
    genres_stream.write( CollectionType(4, 110, "Malbruce") )

    for data in genres_stream.read(pos):
        print(data)

    data = genres_stream.read_all()
    print(data)

    genres_stream.close()

t1()

# block_size % item_size = items_per_block