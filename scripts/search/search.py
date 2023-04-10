# type imports
from scripts.io.serial import Serial
from scripts.io.blocks import Blocks
from scripts.search.moviestrie import MoviesTrie, TrieData
from scripts.search.titlestrie import TitlesTrie
from scripts.types import CollectionType, MovieType, TitleType, MovieBaseDict
# module imports
from scripts.search.controls import found_in_entity, by_name
from scripts.utils import exclusive_union
# const imports
from scripts.config import MOVIESTRIE, TITLESTRIE

class Searcher:
    # tries 
    trie_movies: MoviesTrie
    trie_titles: TitlesTrie
    # serial streams
    stream_titles: Serial
    stream_movies: Serial
    stream_genres: Serial
    stream_decades: Serial
    stream_countries: Serial
    stream_companies: Serial
    # blocks stream
    blocks_genres: Blocks
    blocks_decades: Blocks
    blocks_countries: Blocks
    blocks_companies: Blocks
    # stream 'manager' to easily open/close serial streams
    stream_manager: list[Serial]
    # saves the collections data
    data_genres: list[CollectionType]
    data_decades: list[CollectionType]
    data_countries: list[CollectionType]
    data_companies: list[CollectionType]

    def __init__(self):
        self.trie_movies = None
        self.trie_titles = None
        # initialize the movies and titles stream (r/w entity file)
        self.stream_movies      = Serial('movies', MovieType)
        self.stream_titles      = Serial('titles', TitleType)
        # initialize the collection streams (r/w entity file)
        self.stream_genres      = Serial('genres', CollectionType)
        self.stream_countries   = Serial('countries', CollectionType)
        self.stream_companies   = Serial('companies', CollectionType)
        self.stream_decades     = Serial('decades', CollectionType)
        # initialize the blocks stream (r/w blocks file)
        self.blocks_genres      = Blocks('genres')
        self.blocks_decades     = Blocks('decades')
        self.blocks_countries   = Blocks('countries')
        self.blocks_companies   = Blocks('companies')
        # initialize the collections data
        self.data_genres = []
        self.data_decades = []
        self.data_countries = []
        self.data_companies = []

        self.stream_manager = [\
            self.stream_movies, self.stream_titles, \
            self.stream_genres, self.stream_decades, \
            self.stream_countries, self.stream_companies, \
            self.blocks_genres, self.blocks_decades, \
            self.blocks_countries, self.blocks_companies
        ]

    # open all streams and load the collectiond data
    def load(self):
        self.trie_movies = MoviesTrie.load(MOVIESTRIE)
        self.trie_titles = TitlesTrie.load(TITLESTRIE)
        for stream in self.stream_manager: stream.open()
        # load the collections data
        self.data_genres    = self.stream_genres.read_all()
        self.data_decades   = self.stream_decades.read_all()
        self.data_countries = self.stream_countries.read_all
        self.data_companies = self.stream_companies.read_all()

    # close all streams
    def unload(self):
        for stream in self.stream_manager: stream.close()

    def search_collection(self, data_list:list[CollectionType], item: str, blocks: Blocks) -> list[tuple[int, TrieData]]:
        result_list = []
        # verify if we have the decade passed
        item_found: CollectionType = found_in_entity(\
            data_list, item, by_name \
        )
        # if there is, then we continue with the next steps
        if item_found is not None:
            # read the block for the decade passed
            # and get all the movies IDs of this entry
            block_data = blocks.read_data(item_found.block_pos)
            # iterate through each ID 
            # and get a list of each ID position in the movies entity
            for id in block_data:
                movie_found:tuple(int, TrieData) = \
                    self.trie_movies.search(id)
                if movie_found is not None:
                    result_list.append(movie_found)
        return result_list


    def movie_search(self, name: str, decade: str, genre: str, country: str, company: str) -> list[MovieBaseDict]:
        # uses None as default value so it facilitates the 
        # union proccess

        # list of results for each attribute for search
        result_titles:  dict[int, str] = None
        result_movies:  dict[int, TrieData] = None
        # results for the ids
        result_decade:  dict[int, TrieData] = None
        result_genre:   dict[int, TrieData] = None
        result_country: dict[int, TrieData] = None
        result_company: dict[int, TrieData] = None

        # get all the results for the title
        if name != 'None' and len(name) > 0:
            result_titles = self.trie_titles.search(name) or []
            result_titles = dict(result_titles)
        
        # get all the results for the decade
        if decade != 'None' and len(decade) > 0: 
            result_decade = self.search_collection(\
                self.data_decades, decade, self.blocks_decades \
            )
            result_decade = dict(result_decade)

        # get all the results for the genre
        if genre != 'None' and len(genre) > 0: 
            result_genre = self.search_collection(\
                self.data_genres, genre, self.blocks_genres \
            ) 
            result_genre = dict(result_genre)

        # get all the results for the country
        if country != 'None' and len(country) > 0: 
            result_country = self.search_collection(\
                self.data_countries, country, self.blocks_countries \
            )
            result_country = dict(result_country)

        # get all the results for the company
        if company != 'None' and len(company) > 0: 
            result_company = self.search_collection(\
                self.data_companies, company, self.blocks_companies \
            ) 
            result_company = dict(result_company)

        # merge the results for the movies IDs
        result_movies = exclusive_union(\
            exclusive_union(result_decade, result_genre),   \
            exclusive_union(result_country, result_company) \
        )

        _movies: list[MovieBaseDict] = []

        # searching with attributes will result in any value but 'None'
        # so we must be cautious if 'result_movies' is 'None'
        # because 'exclusive_union' will get all values from 'result_titles'
        # and it does not have the pos of the movie
        if result_movies is not None and result_titles is not None:
            print("search for attr and title")

            # generate the union of titles and movie ids
            result_titles = exclusive_union(result_movies, result_titles)
            result_movies = exclusive_union(result_titles, result_movies)
            
            for movie_id in result_movies.keys():
                movie_pos: int = result_movies[movie_id]['offset']

                _info: MovieType = self.stream_movies.read_item(movie_pos)
                if _info is None: continue

                data: MovieBaseDict = {
                    'id': movie_id,
                    'title': result_titles[movie_id], 
                    'duration': _info.duration,
                    'release_year': _info.release_year,
                    'rating': _info.rating,
                    'genres': result_movies[movie_id]['genres'],
                    'countries': result_movies[movie_id]['countries'],
                    'companies': result_movies[movie_id]['companies']
                }
                _movies.append(data)

        # if we are not searching using titles, only attributes
        elif result_movies is not None:
            print("search only for attr")

            for movie_id in result_movies.keys():
                movie_pos: int = result_movies[movie_id]['offset']
                print(movie_pos)
                _info: MovieType = self.stream_movies.read_item(movie_pos)
                print(_info)
                if _info is None: continue
                
                _title: TitleType = \
                    self.stream_titles.read_item(_info.title_pos)
                print(_title, "end")
                if _title is None: continue

                data: MovieBaseDict = {
                    'id': movie_id,
                    'title': _title.name, 
                    'duration': _info.duration,
                    'release_year': _info.release_year,
                    'rating': _info.rating,
                    'genres': result_movies[movie_id]['genres'],
                    'countries': result_movies[movie_id]['countries'],
                    'companies': result_movies[movie_id]['companies']
                }
                _movies.append(data)
            
        # if we are not searching using attributes, only title
        elif result_titles is not None:
            print("search only for title")
            
            for movie_id in result_titles.keys():
                _info_trie: TrieData = self.trie_movies.search(movie_id)
                if _info_trie is None: continue
                _info_trie = _info_trie[1]
                
                movie_pos = _info_trie['offset']
                _info: MovieType = self.stream_movies.read_item(movie_pos)
                if _info is None: continue

                data: MovieBaseDict = {
                    'id': movie_id,
                    'title': result_titles[movie_id], 
                    'duration': _info.duration,
                    'release_year': _info.release_year,
                    'rating': _info.rating,
                    'genres': _info_trie['genres'],
                    'countries': _info_trie['countries'],
                    'companies': _info_trie['companies']
                }
                _movies.append(data)
        
        # no attributes or titles set for search
        else: return []

        return _movies
        
            
