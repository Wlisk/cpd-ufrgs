# type import
from scripts.io.iobase                  import IOBase
from scripts.io.serial                  import Serial
from scripts.io.blocks                  import Blocks
from scripts.search.moviestrie          import MoviesTrie
from scripts.search.titlestrie          import TitlesTrie
from scripts.types                      import MovieType, CollectionType
# module imports
from scripts.utils                      import wich_decade
from scripts.proccess.readmovies_csv    import readmovies_csv
from scripts.binaries.collections       import generate_blocks
# const imports
from scripts.config                 import CSVFILE, MOVIESTRIE, TITLESTRIE

# 
def generate_binaries():
    # initialize the movies and title streams (r/w entity file)
    movies_stream       = Serial('movies', MovieType)
    # initialize the collection streams (r/w entity file)
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

    # create a collections stream "manager" 
    # to "automatically" open/close the streams
    stream_c_manager: list[tuple[Serial, dict[str, list[int]]]] = [ \
        (genres_stream,       genres), \
        (countries_stream, countries), \
        (companies_stream, companies), \
        (decades_stream,     decades)  \
    ]

    # open entity files and load their content, it'll be used to
    # verify and check if an item is already in the entity file
    for stream, _dict in stream_c_manager: 
        stream.open()
        items: list[CollectionType] = stream.read_all()
        # add to the dict the item name as key and create a new list for it
        for item in items:
            _dict[item.name] = []
        stream.close()

    # open movies stream
    movies_stream.open()

    #! just for test purposes
    max_idx: int    = 50
    
    movies: MoviesTrie = MoviesTrie.load(MOVIESTRIE)
    titles: TitlesTrie = TitlesTrie.load(TITLESTRIE)

    # iterate through all movies and add their info into the entity files
    # notice that only title and movie entity files are write into
    for movie in readmovies_csv(CSVFILE):
        # check if a movie is not already added
        # based on its movie id
        result = movies.search(movie['id'])
        if result is not None: continue

        # write the movie into its respective entity file
        _movie = MovieType(\
            movie['id'], movie['release_year'], \
            movie['duration'], movie['rating'] \
        )
        movie_pos: int = movies_stream.write(_movie)

        # add the movie to the Tries
        movies.add(movie['id'], movie_pos)
        titles.add(movie['id'], movie['title'])

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

    # close the movies stream
    movies_stream.close()
    # save the Tries into disk
    movies.save()
    titles.save()

    # create a list to enable us to iterate through a generic loop 
    # for all collections, so it does not need code repetition
    # we have a dict, each key witha list of IDs
    # and we have a blocks stream and a serial stream
    collections: list[tuple[dict[str|int, list[int]], Blocks, Serial]] = [\
        (genres,    Blocks('genres'),       genres_stream), \
        (countries, Blocks('countries'), countries_stream), \
        (companies, Blocks('companies'), companies_stream), \
        (decades,   Blocks('decades'),     decades_stream)  \
    ]

    generate_blocks(collections)