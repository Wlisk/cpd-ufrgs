# type imports
from typing import Callable
from scripts.types import CollectionType, AllEType

#--------------------------------------------------------------------#
# COMPARE FUNCTIONS
def by_id(e: AllEType, v: int): return e.id == v
def by_name(e: CollectionType, v: str): return e.name == v

#--------------------------------------------------------------------#
# SEARCH FUNCTIONS

# searchs in an entity list for the value given using a compare function
# to verifie if the items match
# return the item if found, or None otherwise
def found_in_entity(entity: list[AllEType], value: int|str, compare_fn: Callable[[AllEType, int|str], bool]) -> AllEType:
    for item in entity:
        if compare_fn(item, value): return item
    return None
