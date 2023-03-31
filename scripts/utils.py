# type imports
from scripts.types import CollectionType
from typing import Any, Generator

from ast import literal_eval    # parse/eval string into python object

NOT_FOUND = -1

# COMPARE FUNCTIONS
def search_by_id(e: CollectionType, v: int): return e.id == v
def search_by_name(e: CollectionType, v: str): return e.name == v

# converts a string of bytes into python string
def bytes_to_str(data: bytes) -> str:
    # split at the first '\0' 
    # and return the first splited part converted as string
    return str( data.split(b'\0', 1)[0], 'utf-8' )

# converts a string to a string of bytes
def str_to_bytes(data: str) -> bytes:
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
    return [item['name'] for item in l]

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





