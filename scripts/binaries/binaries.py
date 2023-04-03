# type import
from scripts.types import MovieType, TitleType, CollectionType, BlockType
from scripts.io.iobase import IOBase

from scripts.proccess.readmovies_csv import readmovies_csv
from scripts.config import CSVFILE
from scripts.io.serial import Serial
from scripts.io.blocks import Blocks
from scripts.utils import wich_decade
from struct import pack


def generate_binaries():
    # initialize the streams to open and read entity files
    movies_stream       = Serial('movies', MovieType)
    titles_stream       = Serial('titles', TitleType)

    # create a dict for each collection type entity
    # dicts don't allow repetitive keys
    # so it'll enable us manage/skip repetitive collection items directly
    genres:     dict[str, list[int]] = dict()
    countries:  dict[str, list[int]] = dict()
    companies:  dict[str, list[int]] = dict()
    decades:    dict[int, list[int]] = dict()

    # create a stream "manager" to "automatically" open/close the streams
    stream_manager: list[IOBase] = [ movies_stream, titles_stream ]
    # open all streams 
    for stream in stream_manager: stream.open()

    # TODO: open entity files and load their content, into the entities
    # it'll be used to verifie and check if an item is already in the file

    # TODO: get id from the last movie in the titles or movie entity
    # so we load it and start the id from that position plus 1
    idx = 1

    # iterate through all movies and add their info into entity files
    # notice that only title and movie entity files are write 
    for movie in readmovies_csv(CSVFILE):
        # TODO: check if a movie is not already added
        # based on its movie id, or title

        # write the title into its respective entity file
        _title = TitleType(idx, movie['id'], movie['title'])
        title_pos: int = titles_stream.write(_title)

        # write the movie into its respective entity file
        _movie = MovieType(\
            idx, title_pos, movie['release_year'], \
            movie['duration'], movie['rating'] \
        )
        movies_stream.write(_movie)

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

    # close all streams opened
    for stream in stream_manager: stream.close()

    # initialize the collection streams to open and read entity files
    genres_stream       = Serial('genres', CollectionType)
    countries_stream    = Serial('countries', CollectionType)
    companies_stream    = Serial('companies', CollectionType)
    decades_stream      = Serial('decades', CollectionType)
    # initialize the streams for blocks management
    genres_block        = Blocks('genres')
    countries_block     = Blocks('countries')
    companies_block     = Blocks('companies')
    decades_block       = Blocks('decades')

    # create a stream "manager" to "automatically" open/close the streams
    stream_manager: list[IOBase] = [\
        genres_stream, countries_stream, companies_stream, decades_stream, \
        genres_block, countries_block, companies_block, decades_block \
    ]
    # open all collection streams 
    for stream in stream_manager: stream.open()

    # create a list to enable us to iterate through a generic loop 
    # for all collections, so it does not need code repetition
    collections: list[tuple[dict[str|int, list[int]], Blocks, Serial]] = [\
        (genres,    genres_block,       genres_stream), \
        (countries, countries_block, countries_stream), \
        (companies, companies_block, companies_stream), \
        (decades,   decades_block,     decades_stream)
    ]

    # loop through the collections
    for collection in collections:
        # TODO: idx should be based on the last item in the entity file
        # so we must load it from the file first
        idx = 1
        _dict, _block, _stream = collection
        for item in _dict.keys():
            # TODO: check if a block for this item already exists
            # before creating a new block
            # TODO: check if the item is already in the entitity file
            # if it is, continue to the next item
            print(item, _block._filename)
            block_pos: int = _block.create()
            block_id: int = 1

            c = CollectionType(idx, block_pos, item)
            _stream.write(c)
            block = BlockType.new(block_id)
            data = _dict[item]
            block.data = pack(f'<{len(data)}I', *data)
            _block.write(block_pos, block)
            block_id += 1

    # close all collection streams opened
    for stream in stream_manager: stream.close()