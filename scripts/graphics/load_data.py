# type imports
from scripts.io.serial import Serial
from scripts.types import CollectionType
from typing import TypedDict

# type for the dicts of select button data
class SelectsData(TypedDict):
    genres: list[str]
    decades: list[str]
    countries: list[str]
    companies: list[str]

def load_data() -> SelectsData: 
    # stream to read the entities file
    genres_stream       = Serial('genres', CollectionType)
    decades_stream      = Serial('decades', CollectionType)
    countries_stream    = Serial('countries', CollectionType)
    companies_stream    = Serial('companies', CollectionType)

    # stream 'manager' to 'automatically' open/close the streams
    stream_manager: list[Serial] = [\
        genres_stream, decades_stream,     \
        countries_stream, companies_stream \
    ]
    for stream in stream_manager: stream.open()

    # default value for the selects button
    genres      = ['None']
    decades     = ['None']
    countries   = ['None']
    companies   = ['None']

    # set the values for the selects

    # load the genres
    _genres = genres_stream.read_all()
    if len(_genres) > 0: 
        genres.extend( [item.name for item in _genres] ) 
    # load the decades
    _decades = decades_stream.read_all()
    if len(_decades) > 0:
        decades.extend( [item.name for item in _decades] ) 
    # load the countries
    _countries = countries_stream.read_all()
    if len(_countries) > 0:
        countries.extend( [item.name for item in _countries] ) 
    # load the companies
    _companies = companies_stream.read_all()
    if len(_companies) > 0:
        companies.extend( [item.name for item in _companies] ) 

    for stream in stream_manager: stream.close()

    return { \
        'genres':       genres,    \
        'decades':      decades,   \
        'countries':    countries, \
        'companies':    companies  \
    }