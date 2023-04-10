# type imports
from typing import Any, Generator
# module imports 
from ast    import literal_eval    # parse/eval string into python object
from struct import pack, unpack
# const imports
from scripts.config \
    import DEV, DATA_DIR, MAX_YEAR, MIN_YEAR, TEST_DIR, INT_SIZE

#--------------------------------------------------------------------#
# converts a string of bytes into python string
def bytes_to_str(data: bytes|bytearray) -> str:
    # split at the first '\0' 
    # and return the first splited part converted as string
    return str( data.split(b'\0', 1)[0], 'utf-8' )

# converts a string to a string of bytes
def str_to_bytes(data: str) -> bytes:
    if type(data) != str: return data
    return bytes(data, 'utf-8')

#--------------------------------------------------------------------#
# cast a data in a string into the given 'cast'
# if a error occurr returns a default value
def safe_parse(_str: str, cast_to: Any, default=None) -> Any:
    try: return cast_to(_str)
    except: return default

# parse a object in a string into a list of dictionaries
def parse_str_to_listdict(_str:str) -> list[dict]: 
    try: return literal_eval(_str)
    except: return [{}]

# gets a year from an string (year-month-day format)
def parse_get_year(_str: str) -> int: 
    return _str.split('-')[0]
    
# gets a list of names (strings) from a list of objects inside a string
def parse_get_names(_str: str) -> list[str]:
    l = parse_str_to_listdict(_str)
    if type(l) == list and len(l) > 0 and type(l[0]) == dict:
        return [item['name'] for item in l]
    return []

# converts a number string into integer
def parse_int(_str: str) -> int:
    return safe_parse(_str, int, 0)

# converts a number string into decimal (float)
def parse_float(_str: str) -> float:
    return safe_parse(_str, float, 0.0)

#--------------------------------------------------------------------#
# gets one of the functions based on the project mode (dev or prod)
# the function is used to get the name of an entity file (who = serial)
# or a block file (who = Any)
if DEV:
    def get_filename(name: str, who: str) -> str:
        if who == 'serial':
            return f'{TEST_DIR}/{name}.test.dat'
        return f'{TEST_DIR}/{name}.blocks.test.dat'
else:
    def get_filename(name: str, who: str) -> str:
        if who == 'serial':
            return f'{DATA_DIR}/{name}.dat'
        return f'{DATA_DIR}/{name}.blocks.dat'

#--------------------------------------------------------------------#
# verifies wich decade the year is to be put into
# returns the year with the last digit turn into 0
def wich_decade(year: int) -> int:
    return (year - year % 10) \
        if (MIN_YEAR <= year <= MAX_YEAR) else 0

#--------------------------------------------------------------------#
# converts a list of integers into its representation in binary 
# each integer occupies 4 bytes in memory
def u32list_to_bytes(u32_list: list[int]) -> bytearray:
    #create a buffer to save the list of numbers
    buffer = bytearray(len(u32_list) * INT_SIZE)
    # allow direct memory access to the buffer
    # notice that python without this direct access
    # would cause extra allocations of memory when using slice
    mem_buffer = memoryview(buffer)
    
    # loop through each number and put then into the buffer
    # with the number correctly converted to be save
    offset = 0
    for u32 in u32_list:
        mem_buffer[offset:offset+4] = pack("<I", u32)
        offset += 4

    return buffer

# converts a list of bytes into a list of integers
# for each 4 bytes, convert into an integer
def bytes_to_u32list(bin: bytes|bytearray, num_ints: int) -> list[int]:
    # allow direct memory access to the buffer
    mem_buffer = memoryview(bin)

    # unpack all the integers from the buffer
    return list( unpack(f"<{num_ints}I", mem_buffer) )

#--------------------------------------------------------------------#
# return a dict union of two dicts
# if there is diffeent values for the same key, 
# then update the key value with the second dict key value
def exclusive_union(dict_1: dict, dict_2: dict) -> dict:
    # check if the dicts are valid dicts
    if dict_1 is None: return dict_2
    if dict_2 is None: return dict_1
    # add keys that are in both dicts
    ex_union = { \
        key: dict_1[key] \
        for key in dict_1 if key in dict_2 \
    } 
    # update the values so it'll have the values of the second dict
    ex_union.update({ \
        key: dict_2[key] \
        for key in dict_2 if key in dict_1 \
    }) 
    return ex_union
