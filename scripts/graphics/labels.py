import tkinter as tk
from tkinter import Tk, Label, Entry, StringVar, OptionMenu, Text, Scrollbar
# const imports
from scripts.graphics.controls import \
    VERTICAL_DISTANCE, HORIZONTAL_DISTANCE, \
    WIDGET_WIDTH, RESULT_AREA_HEIGHT, RESULT_AREA_WIDTH, STYLE

# label for the movie title
def label_movie_title(root: Tk) -> Entry:
    Label(root, text="Movie Title:", **STYLE)\
        .grid(row=0, column=0, pady=VERTICAL_DISTANCE, padx=HORIZONTAL_DISTANCE, sticky="w")
    name_entry = Entry(root, **STYLE)
    name_entry.grid(\
        row=0, column=1, pady=VERTICAL_DISTANCE, padx=HORIZONTAL_DISTANCE, sticky="ew" \
    )
    return name_entry

# label to select available decades
def label_decades(root: Tk, decades: list[str]) -> tuple[StringVar, OptionMenu]:
    tk.Label(root, text="Release Decade:", **STYLE)\
        .grid(row=1, column=0, pady=VERTICAL_DISTANCE, padx=HORIZONTAL_DISTANCE, sticky="w")
    selected_decade = StringVar(root, value=decades[0])
    decade_dropdown = OptionMenu(root, selected_decade, *decades)
    decade_dropdown.config(width=WIDGET_WIDTH, **STYLE)
    decade_dropdown.grid(\
        row=1, column=1, pady=VERTICAL_DISTANCE, padx=HORIZONTAL_DISTANCE, sticky="ew" \
    )
    return (selected_decade, decade_dropdown)

# label to select available genres
def label_genres(root: Tk, movie_genres: list[str]) -> tuple[StringVar, OptionMenu]:
    tk.Label(root, text="Movie Genre:", **STYLE)\
        .grid(row=2, column=0, pady=VERTICAL_DISTANCE, padx=HORIZONTAL_DISTANCE, sticky="w")
    selected_movie_genre = StringVar(root, value=movie_genres[0])
    movie_genre_dropdown = OptionMenu(root, selected_movie_genre, *movie_genres)
    movie_genre_dropdown.config(width=WIDGET_WIDTH, **STYLE)
    movie_genre_dropdown.grid(\
        row=2, column=1, pady=VERTICAL_DISTANCE, padx=HORIZONTAL_DISTANCE, sticky="ew" \
    )
    return (selected_movie_genre, movie_genre_dropdown)

#  label to select available countries
def label_countries(root: Tk, countries: list[str]) -> tuple[StringVar, OptionMenu]:
    tk.Label(root, text="Release Country:", **STYLE)\
        .grid(row=3, column=0, pady=VERTICAL_DISTANCE, padx=HORIZONTAL_DISTANCE, sticky="w")
    selected_country = tk.StringVar(root, value=countries[0])
    country_dropdown = tk.OptionMenu(root, selected_country, *countries)
    country_dropdown.config(width=WIDGET_WIDTH, **STYLE)
    country_dropdown.grid(\
        row=3, column=1, pady=VERTICAL_DISTANCE, padx=HORIZONTAL_DISTANCE, sticky="ew" \
    )
    return (selected_country, country_dropdown)

# label to select available companies
def label_companies(root: Tk, companies: list[str]) -> tuple[StringVar, OptionMenu]:
    tk.Label(root, text="Production Company:", **STYLE)\
        .grid(row=4, column=0, sticky="w", padx=HORIZONTAL_DISTANCE, pady=VERTICAL_DISTANCE)
    selected_company = tk.StringVar(root)
    selected_company.set(companies[0]) 
    company_dropdown = tk.OptionMenu(root, selected_company, *companies)
    company_dropdown.config(width=WIDGET_WIDTH, **STYLE)
    company_dropdown.grid(\
        row=4, column=1, padx=HORIZONTAL_DISTANCE, pady=VERTICAL_DISTANCE, sticky="ew" \
    )
    return (selected_company, company_dropdown)

# label to show the movies results
def label_result(root: Tk) -> tuple[Label, Text]:
    label_result = Label(root, text="Search result:", **STYLE)
    label_result.grid( \
        row=8, column=0, sticky="w", padx=HORIZONTAL_DISTANCE, pady=VERTICAL_DISTANCE \
    )
    text_result = Text(root, height=RESULT_AREA_HEIGHT, width=RESULT_AREA_WIDTH)
    text_result.grid(\
        row=9, column=0, columnspan=2, padx=HORIZONTAL_DISTANCE, pady=VERTICAL_DISTANCE \
    )
    scrollbar = Scrollbar(root, command=text_result.yview)
    scrollbar.grid(row=9, column=2, sticky='ns')
    text_result['yscrollcommand'] = scrollbar.set
    return (label_result, text_result)