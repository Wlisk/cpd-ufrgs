# type imports 
from typing import Callable, Final
# const imports
from scripts.config import MIN_VOTES, MIN_VOTES_COUNT, MAX_TITLE_SIZE
from scripts.io.controls import \
    SIZE_GENRE, SIZE_COUNTRY, SIZE_COMPANY, SIZE_DECADE
# module imports
from scripts.utils \
    import parse_get_names, parse_get_year, parse_int, parse_float

# ignore (not add) columns of the raw movie (movie read from csv)
IGNORE_COLUMNS: Final[ list[str] ] = [
    'adult',
    'belongs_to_collection',
    'homepage',
    'original_title',
    'poster_path',
    'video',
    'budget',
    'original_language',
    'imdb_id',
    'overview',
    'popularity',
    'revenue',
    'spoken_languages',
    'status',
    'tagline',
    'vote_count'
]

# used to skip a movie if the conditions are met 
FILTERS: Final[ dict[str, Callable[[str], bool]] ] =  {
    'adult':        lambda v: v and v == 'True',
    'vote_average': lambda v: v and parse_float(v) <= MIN_VOTES,
    'vote_count':   lambda v: v and parse_int(v) <= MIN_VOTES_COUNT,
    'title':        lambda v: v and len(v) >= MAX_TITLE_SIZE,
    'release_date': lambda v: v and not ('-' in v),
    'genres': \
        lambda v: v and (len(v) == 0 or type(v) != str),
    'production_countries': \
        lambda v: v and (len(v) == 0 or type(v) != str),
    'production_companies': \
        lambda v: v and (len(v) == 0 or type(v) != str)
}

# used to rename a column from the movie dictionary
RENAME_COL: Final[ dict[str, str] ] = {
    'production_countries': 'countries',
    'production_companies': 'companies',
    'release_date':         'release_year',
    'runtime':              'duration',
    'vote_average':         'rating'
}

# parse/modify a data string from the raw movie into a more desirable type
PROCCESS: Final[ dict[str, Callable[[str], int|float|list[str]]] ] = {
    'genres':       parse_get_names,
    'companies':    parse_get_names,
    'countries':    parse_get_names,
    'release_year': parse_get_year,
    'id':           parse_int,
    'duration':     parse_float,
    'rating':       parse_float
} 

# second filter to be used after executing PROCCESS
# used to skip a movie if the conditions are met 
SND_FILTERS: Final[ dict[str, Callable[[list[str]], bool]] ] = { \
    'genres': lambda l: any(len(v) >= (SIZE_GENRE-2) for v in l), \
    'companies': \
        lambda l: any(len(v) >= (SIZE_COUNTRY-2) for v in l), \
    'countries': \
        lambda l: any(len(v) >= (SIZE_COMPANY-2) for v in l), \
}
