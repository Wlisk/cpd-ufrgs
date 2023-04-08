# type imports
from typing import Callable, Any
from scripts.types import CollectionType, AllEType

# COMPARE FUNCTIONS
def by_id(e: AllEType, v: int): return e.id == v
def by_name(e: CollectionType, v: str): return e.name == v


def found_in_entity(entity: list[AllEType], value: int|str, compare_fn: Callable[[AllEType, int|str], bool]):
    for item in entity:
        if compare_fn(item, value): return True
    return False
