import struct
from scripts.binaries.controls import ENTITY, EntityInfo
from scripts.utils import NOT_FOUND
from scripts.entity.io import write_to_end
from scripts.types import MovieBaseDict

# realize a search in the entity file for the given item
# returns the item id if found or NOT_FOUND otherwise
def search_in_entity(entity_file, item_to_search):
    pass

# write item at the end of the entity file
# ?or ordered using a sort algorithm
def write_into_entity(entity_file, item_to_add):
    pass

# table of entities [ Companies, Titles, Genres, Countries and Movies]
def add_to_entity(entity_name: str, movie: MovieBaseDict):
    entity = ENTITY[entity_name]
    items = list(movie[entity.from_column])

    with open(entity.filename, 'rb+') as entity_file:
        for item in items:
            found = search_in_entity(entity_file, item)
            
            # if data found in the entity table, then skip
            if found != NOT_FOUND: continue

            # if not, then we write it to the entity file
            write_into_entity(entity_file, item)
