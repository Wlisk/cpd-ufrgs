#!/usr/bin/python

import csv
from scripts.entity.generate_entities import add_to_entity
from scripts.binaries.controls import ENTITY

movies_file = 'datasets/movies.csv'
limiter = 0#64

with open(movies_file, 'r') as csvrfile:
    # initializes the csv proccessor
    moviesreader = csv.DictReader(csvrfile)

    i = 0   # counter
    n = 1 << limiter
    #entities = ENTITY.keys()

    # iterate through every row and get the movie data
    for movie in moviesreader:
        # exit if limit reached
        if i >= n: break
        i += 1

        for entity in entities:
            add_to_entity(entity, movie)

        print(movie)