# importing types
from io import BufferedReader
from typing import Callable
from scripts.types import EntityInfo, BaseType, HeaderType, AllType
from dataclasses import astuple

import struct
from scripts.binaries.controls import HEADER, ENTITY
from scripts.utils import NOT_FOUND, convert_to_bin
#list.reduce

def convert_to_bin(entity: EntityInfo, data: AllType) -> bytes:
    # convert the BaseType to dict so we can change its data (if needed)
    d = astuple(data)
    
    # if an element of an item is a string, them convert it to bytes
    for key in data:
        if type(data[key]) == str:
            data[key] = str_to_bytes(data[key])

    # get as a list only the values from the dictionary
    values = list(data.values())
    # convert those values into a binary pack based on the format of the entity
    # ATTENTION: notice that the order of the elements in list values follow the order of the elements in the BaseType/dict
    # *list is a python synthax to pass a list of arguments to a dynamic arguments function
    return struct.pack(entity.struct_format, *values)


# returns the n-th item from the entity file
def read_data_from_index(entity_file: BufferedReader, entity: EntityInfo, index: int) -> BaseType:
    # tems are at index n minus one
    index = (index - 1) if index > 0 else 0
    # computes the position based on the size of each item
    pos = HEADER.struct_size + (index * entity.struct_size)
    # get the data at that position
    return read_data_at(entity_file, entity, pos)

# search for an item based on its data
# returns the position of the item in the entity file
# uses a callback function to compare the data in the item and search_value
# type Callable[[list of arg types], return type]
def search_data(entity_file: BufferedReader, entity: EntityInfo, search_value: str|int, compare_fn: Callable[[BaseType, str|int], bool]) -> int:
    for e in read_data(entity_file, entity):
        # if true return the pos of the current item
        if compare_fn(e, search_value): 
            return (entity_file.tell() - entity.struct_size)
    return NOT_FOUND







# the '|' can be used to merge dict (union operation, only for dicts)