# type imports 
from typing import Callable  

from scripts.utils \
    import parse_get_name, parse_get_year, parse_int, parse_float

MIN_VOTES = 6.0
MIN_VOTE_COUNT = 10
MAX_TITLE_SIZE = 150 - 1

# ignore (not add) columns of the raw movie
IGNORE_COLUMNS = [
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
FILTERS: dict[str, Callable[[str], bool]] =  {
    'adult':        lambda v: v and v == 'True',
    'vote_average': lambda v: v and parse_float(v) <= MIN_VOTES,
    'vote_count':   lambda v: v and parse_int(v) <= MIN_VOTE_COUNT,
    'title':        lambda v: v and len(v) >= MAX_TITLE_SIZE
}

# used to rename a column from the movie dictionary
RENAME_COL = {
    'production_countries': 'countries',
    'production_companies': 'companies',
    'release_date':         'release_year',
    'runtime':              'duration',
    'vote_average':         'rating'
}

# parse/modify a data string from the raw movie into a more desirable type
PROCCESS: dict[str, Callable[[str], int|list[str]]] = {
    'genres':       parse_get_name,
    'companies':    parse_get_name,
    'countries':    parse_get_name,
    'release_year': parse_get_year,
    'id':           parse_int,
    'duration':     parse_float,
    'rating':       parse_float
} 