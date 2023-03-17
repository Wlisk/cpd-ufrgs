import struct

NOT_FOUND = -1

# realize a search in the entity file for the given item
# returns the item id if found or NOT_FOUND otherwise
def search_in_entity(entity_file, item_to_search):
    pass

# write item at the end of the entity file
# ?or ordered using a sort algorithm
def write_into_entity(entity_file, item_to_add):
    pass

# table companies
def add_to_entity_companies(entity_filename, items):
    with open(entity_filename, 'rb+') as entity_file:
        for item in items:
            found = search_in_entity(entity_file, item)
            
            # if data found in the entity table, then skip
            if found != NOT_FOUND: continue

            # if not, then we write it to the entity file
            write_into_entity(entity_file, item)


