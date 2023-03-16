#!/usr/bin/python

import csv          # used to read, write and proccess csv files
import json         #   

csvfilename = "datasets/raw/movies_metadata.csv"
csvwritefile = "datasets/movies.csv"
datahead = []
rowscount = 0

movies_matadata_format = [
    'adult',                    # filter: True - (True/False)
    'belongs_to_collection',    # ignore table - (json)
    'budget',                   # (integer)
    'genres',                   # (list json = [{"id", "name"}]) 
    'homepage',                 # ignore table - (urls)
    'id',                       # tmdb identifier - (integer)
    'imdb_id',                  # imdb identifier - (integer)
    'original_language',        # (char[3] = two letters language identifier + null)
    'original_title',           # (dynamic string)
    'overview',                 # info about the movie - (text, dynamic string)
    'popularity',               # (float/decimal)
    'poster_path',              # ignore table (dynamic string)
    'production_companies',     # (list json = [{"name", "id"}])
    'production_countries',     # (list json = [{"iso_3166_1", "name"} = 
                                #   (char[3] 2 letters contry identifier + null, 
                                #   dynamic string country name)] )
    'release_date',             # (date = numeric year-month-day)
    'revenue',                  # (integer)
    'runtime',                  # execution time - (float/decimal)
    'spoken_languages',         # (list json = [{"iso_639_1", "name"} = 
                                #   (char[3] 2 letters language identifier + null, 
                                #   dynamic string language name)] )
    'status',                   # (Released/Post Production/?)
    'tagline',                  # (dynamic string, text)
    'title',                    # (dynamic string)
    'video',                    # ignore table - (True/False)
    'vote_average',             # rating - (decimal = 0.0 to 10.0)
    'vote_count'                # (integer)
]

MIN_VOTES = 6.0
MIN_VOTE_COUNT = 10
MAX_TITLE_SIZE = 150 - 1

# used to skip a row if the conditions are met 
filters =  {
    'adult': lambda value: value and value == 'True',
    'vote_average': lambda value: value and float(value) <= MIN_VOTES,
    'vote_count': lambda value: value and int(value) <= MIN_VOTE_COUNT,
    'title': lambda value: value and len(value) >= MAX_TITLE_SIZE
}

# ignore (not add) columns to the final table
ignore_columns = [
    'adult',
    'belongs_to_collection',
    'homepage',
    'original_title',
    'poster_path',
    'production_countries',
    'video'
]

with open(csvfilename, 'r') as csvrfile:
    with open(csvwritefile, 'w') as csvwfile:
        # initializes the csv proccessor
        csvreader = csv.DictReader(csvrfile)
        csvwriter = csv.writer(csvwfile)

        # gets the first row of the csv (where is the columns subjectives/columns title)
        # filter the ignored columns
        datahead = [ \
            coltitle for coltitle in csvreader.fieldnames \
            if coltitle not in ignore_columns \
        ]
        csvwriter.writerow(datahead)

        i = 0   # counter
        n = 1<<64   # limiter

        # iterate through every row to get the data from the columns
        for csvrow in csvreader:
            # exit if limit reached
            if i >= n:
                break
            i += 1

            csvrow_proccessed = []
            skip = False

            for colname, value in csvrow.items():
                # test if a column is in the filters, and tries to execute the correspondent function
                # to test the row, otherwise execute the default false-return-function
                if filters.get(colname, lambda v: False)(value):
                    skip = True
                    break

                # jump to other column if column name in ignore list
                if colname in ignore_columns: continue
                # otherwise add column to current row
                csvrow_proccessed.append(csvrow[colname])

            # jump row if row match any filters
            if skip: continue

            csvwriter.writerow(csvrow_proccessed)
            rowscount += 1

        

print(datahead)
print(rowscount)


## title.principals.tsv
# tconst            - tmdb id (movie id)
# ordering          - ignore column (order of persons)
# nconst            - cast id (person id)
# category          - list or enum of (director, actor, producer, etc.)
# job               - ignore column
# characters        - ignore column

## name.basics.tsv
# nconst            - cast id (person id)
# primaryName       - name of the person
# birthYear         - (integer)
# deathYear         - (integer)
# primaryProfession - ignore column (list of professions)
# knownForTitles    - ignore column (list of movie ids)
