#!/usr/bin/python

import csv
from scripts import generate_entities as ge

movies_file = 'datasets/movies.csv'

class EntityInfo:
    def __init__(self, file, struct_size):
        self.file = file
        self.struct_size = struct_size

entity = {
    'companies':    EntityInfo('data/companies.bin',    0),
    'titles':       EntityInfo('data/titles.bin',       0),
    'genres':       EntityInfo('data/genres.bin',       0),
    'countries':    EntityInfo('data/countries.bin',    0),
    'movies':       EntityInfo('data/movies.bin',       0)
}

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

        # tries to add a data to an entity (companies)
        ge.add_to_entity['companies']( \
            entity['companies'].file, \
            movie['production_companies'] \
        )

        # tries to add a data to an entity (titles)
        ge.add_to_entity['titles']( \
            entity['titles'].file, \
            movie['title'] \
        )

        # tries to add a data to an entity (genres)
        ge.add_to_entity['genres']( \
            entity['genres'].file, \
            movie['genres'] \
        )

        # tries to add a data to an entity (countries)
        ge.add_to_entity['countries']( \
            entity['countries'].file, \
            movie['production_countries'] \
        )

        # tries to add a data to an entity (movies)
        ge.add_to_entity['movies']( \
            entity['movies'].file, \
            movie \
        )

        print(movie)