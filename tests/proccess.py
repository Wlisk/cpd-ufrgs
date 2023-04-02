#!/usr/bin/python

# configure module imports for user created modules outside the scope
import sys, os  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.proccess.readmovies_csv import readmovies_csv

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

csvfilename = "movies_metadata.csv"

for i, movie in enumerate(readmovies_csv(csvfilename)):
    print(movie)
    if i == 0: break
