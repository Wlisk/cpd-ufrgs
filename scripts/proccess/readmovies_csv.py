# type imports
from typing import Generator 
from scripts.types import MovieBaseDict

from csv import DictReader      
from scripts.proccess.controls \
    import FILTERS, IGNORE_COLUMNS, RENAME_COL, PROCCESS

# Generator to loop through a list of movies
def readmovies_csv(csvfilename: str) -> Generator[MovieBaseDict, None, None]:
    with open(csvfilename, 'r') as csvrfile:
        # read csv as a list of dictionaries
        csvreader = DictReader(csvrfile)

        # iterate through every row on the csv to get the movies data
        for csvrow in csvreader:
            movie: MovieBaseDict = {}
            skip: bool = False

            # iterate through all the columns of the row
            for colname, value in csvrow.items():
                # test if a column is in the filters, 
                # and tries to execute the correspondent function, 
                # otherwise execute the default false-return-function
                filters_check = FILTERS.get(colname, lambda v: False)(value)
                if filters_check or filters_check == None:
                    skip = True
                    break

                # jump to other column if column name in ignore list
                if colname in IGNORE_COLUMNS: continue

                # change the name of the column if there is a new one
                # or keep the same column name
                newcolname = RENAME_COL.get(colname, colname)

                if colname == 'release_date':
                    print(csvrow[colname])

                # proccess the data of the column if exists a funtion for this
                # otherwise execute a return-same-value function
                movie[newcolname] = \
                    PROCCESS.get(newcolname, lambda v: v)(csvrow[colname])

            # jump row if row match any filters
            if skip: continue

            # return the current movie as a generator value so we can 
            # iterate through the movies using for-in loop
            yield movie
