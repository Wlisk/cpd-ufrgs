from scripts.entity.entity_info import BaseTuple

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