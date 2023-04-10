#!/usr/bin/python
# module imports
from scripts.binaries.binaries import generate_binaries
# const imports
from scripts.config import CSVFILE

def main():
    load_csv: bool = True

    if load_csv: generate_binaries(CSVFILE)
    

if __name__ == "__main__":
    main()

