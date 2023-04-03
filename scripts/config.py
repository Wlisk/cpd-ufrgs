from os import path
from typing import Final

DEV: Final = True

# proccess
MIN_VOTES: Final = 6.0
MIN_VOTES_COUNT: Final = 10
MAX_TITLE_SIZE: Final = 80 - 1

# binaries 
KB: Final = 1024       # 1KB
MB: Final = 1024 * KB  # 1MB

BLOCK_SIZE: Final = 4*MB

BLOCK_SIGNATURE: Final = -1

# curr folder is script, so using '..' let us outside of script folder
BASE_DIR: Final = path.abspath('.')
DATA_DIR: Final = f'{BASE_DIR}/data'
TEST_DIR: Final = f'{BASE_DIR}/tests/data'
CSVFILE: Final = f'{BASE_DIR}/datasets/movies.csv'

NOT_FOUND: Final = -1

MAX_YEAR: Final = 2060
MIN_YEAR: Final = 1960