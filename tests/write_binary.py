#!/usr/bin/python

# configure module imports for user created modules outside the scope
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# importing types
from collections import namedtuple
from io import BufferedReader

import struct
from scripts.io.controls \
    import EntityInfo, ENTITY, HEADER, EntityTuple, BaseTuple, HeaderTuple
from scripts.entity.io import \
    read_header, read_data, read_data_at, read_data_from_index, \
    search_data, write_to_end, write_at

from scripts.utils import bytes_to_str, convert_to_bin

f = open('genres.test.bin', 'rb')

#print(read_header(f))





    

t = read_data_from_index(f, ENTITY['genres'], 1)
id, name = t
name = bytes_to_str(name)
print(id, name)

print( convert_to_bin(ENTITY['genres'], t) )


f.close()