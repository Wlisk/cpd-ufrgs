# type imports
from typing import Any, Generator

from ast import literal_eval    # parse/eval string into python object
from scripts.config \
    import DEV, DATA_DIR, MAX_YEAR, MIN_YEAR, TEST_DIR, INT_SIZE
from struct import pack

# converts a string of bytes into python string
def bytes_to_str(data: bytes) -> str:
    # split at the first '\0' 
    # and return the first splited part converted as string
    return str( data.split(b'\0', 1)[0], 'utf-8' )

# converts a string to a string of bytes
def str_to_bytes(data: str) -> bytes:
    if type(data) != str: return data
    return bytes(data, 'utf-8')

# 
def safe_parse(v: str, cast_to: Any, default=None) -> Any:
    try: return cast_to(v)
    except: return default

# 
def parse_str_to_listdict(v:str) -> list[dict]: 
    try: return literal_eval(v)
    except: return [{}]

# 
def parse_get_year(v: str) -> int: 
    year_str = v.split('-')[0]
    try: return int(year_str)
    except: return 0
    
# 
def parse_get_names(v: str) -> list[str]:
    l = parse_str_to_listdict(v)
    if len(l) > 0 and type(l[0]) == dict:
        return [item['name'] for item in l]
    return []

def parse_int(v: str) -> int:
    return safe_parse(v, int, 0)

def parse_float(v: str) -> float:
    return safe_parse(v, float, 0.0)

def bin_in_chuncks(bin: bytes, offset: int) -> Generator[bytes, None, None]:
    pos = 0             
    length = len(bin)  
    # while end not reached 
    while pos < length:
        next_pos = pos + offset
        # slice from the current pos plus offset
        yield bin[pos : next_pos]
        pos = next_pos


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


# verifies wich decade the year is to be put into
# returns the year with the last digit turn into 0
def wich_decade(year: int) -> int:
    if not (MIN_YEAR <= year <= MAX_YEAR): return 0
    return year - year % 10

# 1
def u32list_to_bytes(u32_list: list[int]) -> bytearray:
    #create a buffer to save the list of numbers
    buffer = bytearray(len(u32_list) * INT_SIZE)
    # allow direct memory access to the buffer
    # notice that python without this direct access
    # would cause extra allocations of memory when using slice
    mem_buffer = memoryview(buffer)
    buffer = bytearray()
    # loop through each number and put then into the buffer
    # with the number correctly converted to be save
    offset = 0
    for u32 in u32_list:
        mem_buffer[offset:offset+4] = pack("<i", u32)
        offset += 4

    return buffer