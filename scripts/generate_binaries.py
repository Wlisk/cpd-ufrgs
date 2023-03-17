#!/usr/bin/python

import csv

from scripts import generate_entities as ge

movies_file = 'datasets/movies.csv'

entityfile_companies = 'data/companies.bin'

with open(movies_file, 'r') as csvrfile:
    # initializes the csv proccessor
    moviesreader = csv.DictReader(csvrfile)

    i = 0   # counter
    n = 1#<<64   # limiter

    # iterate through every row and get the movie data
    for movie in moviesreader:
        # exit if limit reached
        if i >= n: break
        i += 1

        ge.add_to_entity_companies(movie['production_companies'])

        print(movie)