# type imports
""" from scripts.types import MovieBaseDict


from scripts.binaries.controls import ENTITY, EntityInfo


# table of entities [ Companies, Titles, Genres, Countries and Movies]
def add_to_entity(entity_name: str, movie: MovieBaseDict):
    entity: EntityInfo = ENTITY[entity_name]
    items = movie[entity_name]

    with open(entity.filename, 'rb+') as entity_file:
        for item in items:
            found = search_in_entity(entity_file, item)
            
            # if data found in the entity table, then skip
            if found != NOT_FOUND: continue

            # if not, then we write it to the entity file
            write_into_entity(entity_file, item) """
