# importing types
from io import BufferedReader
from collections.abc import Callable
from scripts.entity.entity_info import EntityInfo, BaseTuple, HeaderTuple

import struct
from scripts.entity.entity_info import HEADER
from scripts.utils import NOT_FOUND, convert_to_bin

# read from an entity file its header data
def read_header(entity_file: BufferedReader) -> HeaderTuple: 
    # guarantees that it's at the init of the file
    entity_file.seek(0)
    # read the header structure data
    header_data = entity_file.read(HEADER.struct_size)
    # generate and return a namedtuple with the data readed within
    return HEADER.namedtuple._make( \
        struct.unpack(HEADER.struct_format, header_data) \
    )

# read from an entity file its data contents
# this function should be used as an iterator
def read_data(entity_file: BufferedReader, entity: EntityInfo) -> BaseTuple:
    # points to the first byte after the header structure
    entity_file.seek(HEADER.struct_size)

    while e := entity_file.read(entity.struct_size):
        # if end of file or cannot read offset bytes further then exit loop
        # as there is no more entity data to read
        if len(e) < entity.struct_size: break

        data = entity.namedtuple._make( \
            struct.unpack(entity.struct_format, e) \
        )

        # if id is equal 0, it means there is no more valid data to read
        if data.id == 0: break

        # returns a generator for the data read
        yield data

# return a data from an entity file at the given position in thee file
def read_data_at(entity_file: BufferedReader, entity: EntityInfo, pos: int) -> BaseTuple:
    # go to the position in the file
    entity_file.seek(pos)
    # read the entity data
    e = entity_file.read(entity.struct_size)
    # return the entity as a namedtuple
    return entity.namedtuple._make( \
        struct.unpack(entity.struct_format, e) \
    )

# returns the n-th item from the entity file
def read_data_from_index(entity_file: BufferedReader, entity: EntityInfo, index: int) -> BaseTuple:
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
def search_data(entity_file: BufferedReader, entity: EntityInfo, search_value: str|int, compare_fn: Callable[[BaseTuple, str|int], bool]) -> int:
    for e in read_data(entity_file, entity):
        # if true return the pos of the current item
        if compare_fn(e, search_value): 
            return (entity_file.tell() - entity.struct_size)
    return NOT_FOUND

# write data at some position in the file
def write_at(entity_file: BufferedReader, entity: EntityInfo, pos: int, data: BaseTuple|dict):
    # goes to the position where the data must be written
    entity_file.seek(pos)
    # converts to a binary packed structure
    bin = convert_to_bin(entity, data)

    entity_file.write(bin)

# update the header of the file with the new data (overwrite all header section)
def update_header(entity_file: BufferedReader, data: HeaderTuple|dict):
    write_at(entity_file, HEADER, 0, data)

# notice that entity_file should be opened in 'rb+' or 'wb+' mode
def write_to_end(entity_file: BufferedReader, entity: EntityInfo, data: BaseTuple|dict):
    # gets data from the header of the file first
    header = read_header(entity_file)

    # with the information, write at the "end" of the file
    write_at(entity_file, entity, header.end_of_file, data)

    # update the header tuple
    # order: 'num_items', 'item_size', 'end_of_file'
    header = header._make([\
        header.num_items + 1, \
        header.item_size, \
        entity_file.tell() \
    ])

    update_header(entity_file, header)