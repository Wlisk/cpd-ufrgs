# type imports
from typing     import Final
# module imports
from os.path    import abspath

#--------------------------------------------------------------------#
# set if we are in development or production mode
DEV: Final = False

NOT_FOUND: Final = -1

#--------------------------------------------------------------------#
# PROCCESS

# filters settings
MIN_VOTES: Final        = 5.0
MIN_VOTES_COUNT: Final  = 10
MAX_TITLE_SIZE: Final   = 80 - 1

#--------------------------------------------------------------------#
# BINARIES 

KB: Final = 1024       # 1KB
MB: Final = 1024 * KB  # 1MB

# blocks constants
BLOCK_SIZE: Final       = 64*KB
BLOCK_BUFFER: Final     = BLOCK_SIZE*b'0' # a 1mb binary buffer
BLOCK_SIGNATURE: Final  = -1

# directories
BASE_DIR: Final = abspath('.')  # project directory (if main.py executed)
DATA_DIR: Final = f'{BASE_DIR}/data'
TEST_DIR: Final = f'{BASE_DIR}/tests/data'

def get_trie_fname(trie_name: str) -> str: 
    return f'{DATA_DIR}/{trie_name}.trie.pickle'

# files
CSVFILE: Final      = f'{BASE_DIR}/datasets/movies.csv'
MOVIESTRIE: Final   = get_trie_fname('movies')
TITLESTRIE: Final   = get_trie_fname('titles')

#--------------------------------------------------------------------#

# minimum and maximum accepted year for a movie
MAX_YEAR: Final = 2060
MIN_YEAR: Final = 1960

# the size of an integer in bytes
INT_SIZE: Final = 4