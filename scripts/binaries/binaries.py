# type import
from scripts.types import MovieType, TitleType, CollectionType, BlockType
from scripts.io.iobase import IOBase

from scripts.proccess.readmovies_csv import readmovies_csv
from scripts.config import CSVFILE, MOVIESTRIE
from scripts.io.serial import Serial
from scripts.io.blocks import Blocks
from scripts.utils import wich_decade, u32list_to_bytes
from struct import pack
from scripts.search.moviestrie import MoviesTrie
from scripts.search.controls import found_in_entity, by_name

# 
def generate_binaries():
    # initialize the streams to open and read entity files
    movies_stream       = Serial('movies', MovieType)
    titles_stream       = Serial('titles', TitleType)
    # initialize the collection streams to open and read entity files
    genres_stream       = Serial('genres', CollectionType)
    countries_stream    = Serial('countries', CollectionType)
    companies_stream    = Serial('companies', CollectionType)
    decades_stream      = Serial('decades', CollectionType)

    # create a dict for each collection type entity
    # dicts don't allow repetitive keys
    # so it'll enable us manage/skip repetitive collection items directly
    genres:     dict[str, list[int]] = dict()
    countries:  dict[str, list[int]] = dict()
    companies:  dict[str, list[int]] = dict()
    decades:    dict[int, list[int]] = dict()

    # create a stream "manager" to "automatically" open/close the streams
    stream_manager: list[IOBase] = [ movies_stream, titles_stream ]
    stream_c_manager: list[tuple[IOBase, dict[str, list[int]]]] = [ \
        (genres_stream,       genres), \
        (countries_stream, countries), \
        (companies_stream, companies), \
        (decades_stream,     decades) \
    ]
    # open all streams 
    for stream in stream_manager: stream.open()

    # open entity files and load their content, it'll be used to
    # verify and check if an item is already in the entity file
    for stream, _dict in stream_c_manager: 
        stream.open()
        items = stream.read_all()
        for item in items:
            _dict[item.name] = []
        stream.close()

    # get id from the num of items in the movies/titles entity file
    idx: int = titles_stream._headerdata.num_items + 1
    max_idx = idx + 10
    
    movies: MoviesTrie = MoviesTrie.load(MOVIESTRIE)

    # iterate through all movies and add their info into entity files
    # notice that only title and movie entity files are write 
    for movie in readmovies_csv(CSVFILE):
        # check if a movie is not already added
        # based on its movie id, or title
        result = movies.search(movie['id'])
        if result is not None: continue

        # write the title into its respective entity file
        _title = TitleType(idx, movie['id'], movie['title'])
        title_pos: int = titles_stream.write(_title)

        # write the movie into its respective entity file
        _movie = MovieType(\
            movie['id'], title_pos, movie['release_year'], \
            movie['duration'], movie['rating'] \
        )
        movie_pos: int = movies_stream.write(_movie)
        movies.add(movie['id'], movie_pos)

        # iterate through each item in the collection
        # if the item is not already in the dict
        # then create a new one with default value as a list
        # and add to it the id of the movie
        for genre in movie['genres']:
            genres.setdefault(genre, []).append(movie['id'])

        for country in movie['countries']:
            countries.setdefault(country, []).append(movie['id'])

        for company in movie['companies']:
            companies.setdefault(company, []).append(movie['id'])
        
        this_decade = wich_decade(movie['release_year'])
        decades.setdefault(this_decade, []).append(movie['id'])

        idx += 1

        if idx == max_idx: break

    # close all streams opened
    for stream in stream_manager: stream.close()
    movies.save()

    # initialize the streams for blocks management
    genres_block        = Blocks('genres')
    countries_block     = Blocks('countries')
    companies_block     = Blocks('companies')
    decades_block       = Blocks('decades')

    # create a list to enable us to iterate through a generic loop 
    # for all collections, so it does not need code repetition
    collections: list[tuple[dict[str|int, list[int]], Blocks, Serial]] = [\
        (genres,    genres_block,       genres_stream), \
        (countries, countries_block, countries_stream), \
        (companies, companies_block, companies_stream), \
        (decades,   decades_block,     decades_stream)
    ]

    print(genres)
    print(countries)
    print(companies)
    print(decades)

    # loop through the collections
    for collection in collections:
        _dict, _block, _stream = collection

        _stream.open()
        _block.open()

        # id's are based on the num of elements in the entities file
        idx: int = _stream._headerdata.num_items + 1

        # read all items from the entity file
        entity_data: list[CollectionType] = _stream.read_all()

        # loop through each collection item found in readmovies_csv
        for item in _dict.keys():
            # check if the item is already in the entitity file
            # if it is not, create a new block for the item
            block_pos = _block._header.struct_size
            found:CollectionType = found_in_entity(entity_data, item, by_name)

            if found is None: 
                # create a new block in the blocks file for this new item
                block_pos: int = _block.create()
                # write the new item into the entity file
                c = CollectionType(idx, block_pos, item)
                _stream.write(c)
                # update the id for the new items to come
                idx += 1
            else: block_pos = found.block_pos

            item_block: BlockType = _block.read(block_pos)

            # add a list of integers into the block
            # if there is new elements (ids)
            if len(_dict[item]): 
                _block.write_into(block_pos, item_block, _dict[item])
                

        _stream.close()
        _block.close()
