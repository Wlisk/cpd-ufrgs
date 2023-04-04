# type import
from scripts.types import MovieType, TitleType, CollectionType, BlockType
from scripts.io.iobase import IOBase

from scripts.proccess.readmovies_csv import readmovies_csv
from scripts.config import CSVFILE, MOVIESTRIE
from scripts.io.serial import Serial
from scripts.io.blocks import Blocks
from scripts.utils import wich_decade
from struct import pack
from scripts.search.moviestrie import MoviesTrie

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
    stream_manager: list[IOBase] = [ \
        movies_stream, titles_stream, \
    ]
    stream_c_manager: list[tuple[IOBase, dict[str, list[int]]]] = [ \
        (genres_stream,       genres), \
        (countries_stream, countries), \
        (companies_stream, companies), \
        (decades_stream,     decades) \
    ]
    # open all streams 
    for stream in stream_manager: stream.open()

    # TODO: open entity files and load their content, it'll be used to
    # verify and check if an item is already in the entity file
    for stream, _dict in stream_c_manager: 
        stream.open()
        items = stream.read_all()
        for item in items:
            _dict[item.name] = []
        stream.close()

    # get id from the last movie in the titles or movie entity
    # so we load it and start the id from that position plus 1
    idx = 1
    last_added = titles_stream.read_last()
    if last_added != None: 
        idx = last_added.id + 1

    max_idx = idx + 10
    
    movies = MoviesTrie.load(MOVIESTRIE)

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
        print(movie['genres'])
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

    print(genres)
    print(countries)
    print(companies)
    print(decades)

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