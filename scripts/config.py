from os import path

# proccess
MIN_VOTES = 6.0
MIN_VOTES_COUNT = 10
MAX_TITLE_SIZE = 80 - 1

# binaries 
KB = 1024       # 1KB
MB = 1024 * KB  # 1MB

BLOCK_SIZE = 4*MB

# curr folder is script, so using '..' let us outside of script folder
BASE_DIR = path.abspath('..')
DATA_DIR = f'{BASE_DIR}/data'