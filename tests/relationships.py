from typing import List
from scripts.entity.entity_info import BaseTuple, EntityInfo, HeaderTuple
import struct

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

class RelationshipInfo(BaseTuple):
    id1: int
    id2: int

class RelationshipTuple(HeaderTuple):
    MODEL = RelationshipInfo
    __slots__ = ()
    struct_format = '<ii'
    size = struct.calcsize(struct_format)
    file_extension = '.rel'
    
def create_relationship_files() -> None:
    # get the list of entities to relate
    entities = ['years', 'companies', 'countries', 'genres']
    # iterate through all possible relationship between the entities
    relationships = list(itertools.combinations(entities, 2))
    for rel in relationships:
        # create the filename for the relationship and open the file
        filename = f"data/{rel[0]}_{rel[1]}.bin"
        with open(filename, 'wb') as f:
            # create a list to store the relationships
            relationships_list = []
            # iterate through all movies to check for relationships
            for movie in movies:
                # get the entities ids for this movie
                entity1_id = movie[f"{rel[0]}_id"]
                entity2_id = movie[f"{rel[1]}_id"]
                # if both entities have an id, add the relationship to the list
                if entity1_id != NOT_FOUND and entity2_id != NOT_FOUND:
                    relationship = RelationshipTuple(entity1_id, entity2_id)
                    relationships_list.append(relationship)
            # sort the relationships and write them to the file
            relationships_list.sort()
            for r in relationships_list:
                f.write(convert_to_bin(RelationshipInfo, r))
