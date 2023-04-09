# importing types
from io import BufferedReader
from typing import Callable
from scripts.types import EntityInfo, BaseType, HeaderType, AllType
from dataclasses import astuple

import struct
from scripts.binaries.controls import HEADER, ENTITY
from scripts.utils import NOT_FOUND, convert_to_bin

#list.reduce

def bin_in_chuncks(bin: bytes, offset: int) -> Generator[bytes, None, None]:
    pos = 0             
    length = len(bin)  
    # while end not reached 
    while pos < length:
        next_pos = pos + offset
        # slice from the current pos plus offset
        yield bin[pos : next_pos]
        pos = next_pos



# search for an item based on its data
# returns the position of the item in the entity file
# uses a callback function to compare the data in the item and search_value
# type Callable[[list of arg types], return type]
def search_data(entity_file: BufferedReader, entity: EntityInfo,
                search_value: str | int,
                compare_fn: Callable[[BaseType, str | int], bool]) -> int:
    for e in read_data(entity_file, entity):
        # if true return the pos of the current item
        if compare_fn(e, search_value):
            return (entity_file.tell() - entity.struct_size)
    return NOT_FOUND


# the '|' can be used to merge dict (union operation, only for dicts)