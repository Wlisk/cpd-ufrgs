# importing types
from io import BufferedReader
from typing import Callable
from scripts.types import EntityInfo, BaseType, HeaderType, AllType
from dataclasses import astuple

import struct
from scripts.binaries.controls import HEADER, ENTITY
from scripts.utils import NOT_FOUND, convert_to_bin

#list.reduce





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