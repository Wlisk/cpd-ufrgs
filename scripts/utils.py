# type imports
from scripts.entity.entity_info import BaseTuple, EntityInfo, HeaderTuple
from typing import Any

import struct
from ast import literal_eval    # parse/eval string into python object

NOT_FOUND = -1

# COMPARE FUNCTIONS
def search_by_id(e: BaseTuple, v: int): return e.id == v
def search_by_name(e: BaseTuple, v: str): return e.name == v

# converts a string of bytes into python string
def bytes_to_str(data: bytes) -> str:
    # split at the first '\0' 
    # and return the first splited part converted as string
    return str( data.split(b'\0', 1)[0], 'utf-8' )

# converts a string to a string of bytes
def str_to_bytes(data: str) -> bytes:
    return bytes(data, 'utf-8')

def convert_to_bin(entity: EntityInfo, data: BaseTuple|dict|HeaderTuple) -> bytes:
    # convert the BaseTuple to dict so we can change its data (if needed)
    if type(data) != dict: data = data._asdict()
    
    # if an element of an item is a string, them convert it to bytes
    for key in data:
        if type(data[key]) == str:
            data[key] = str_to_bytes(data[key])

    # get as a list only the values from the dictionary
    values = list(data.values())
    # convert those values into a binary pack based on the format of the entity
    # ATTENTION: notice that the order of the elements in list values follow the order of the elements in the BaseTuple/dict
    # *list is a python synthax to pass a list of arguments to a dynamic arguments function
    return struct.pack(entity.struct_format, *values)

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