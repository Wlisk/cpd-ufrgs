# type imports
import tkinter as tk
from tkinter import Tk
from scripts.graphics.load_data import SelectsData
from scripts.search.search import Searcher
# module imports
from scripts.types import MovieBaseDict
from scripts.graphics.buttons import generate_button
from scripts.graphics.load_data import load_data
from scripts.graphics.actions import proccess_csv
from scripts.graphics.labels import \
    label_movie_title, label_decades, label_genres, label_countries, label_companies, label_result
# const imports
from scripts.graphics.controls import BACKGROUND, APP_TITLE, APP_SIZE
#############################################                                 

# 
def showable_results(results: list[MovieBaseDict]) -> list[str]:
    _list = []
    for item in results:
        _list.append(\
            f'ID: {item["id"]}\n' + \
            f"Title: {item['title']}\n" + \
            f"Year: {item['release_year']}\n" + \
            f"Rating: {item['rating']}\n" + \
            f"Duration: {item['duration']}min\n" + \
            f"Genres: {item['genres']}\n" + \
            f"Countries: {item['countries']}\n" + \
            f"Companies: {item['companies']}\n" + \
            "----------------------------------------------------\n"
        )
    return _list

class GraphicInterface:
    root: Tk            # the window root
    results: list       # saves the results of the search
    searcher: Searcher  # proccess the search of movies

    def __init__(self, root: Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_SIZE)
        self.root.configure(bg=BACKGROUND)
        self.create_widgets()
        self.results = []
        self.searcher = Searcher()
        self.searcher.load()

    def configure_weights(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        for i in range(10):
            self.root.rowconfigure(i, weight=1)

    def create_widgets(self):
        ##############################################
        data: SelectsData = load_data()
        decades         = data['decades']
        movie_genres    = data["genres"]
        countries       = data["countries"]
        companies       = data["companies"]
        ##############################################
        
        # set the labels and options for the select buttons
        self.name_entry = label_movie_title(self.root)
        self.selected_decade, self.decade_dropdown = \
            label_decades(self.root, decades)
        self.selected_movie_genre, self.movie_genre_dropdown = \
            label_genres(self.root, movie_genres)
        self.selected_country, self.country_dropdown = \
            label_countries(self.root, countries)
        self.selected_company, self.company_dropdown = \
            label_companies(self.root, companies)
        
        # generate the button for executing actions in the window
        self.search_button = \
            generate_button(self.root, "Search", self.show_result, row=6)
        self.reverse_button = \
            generate_button(self.root, "Reverse", self.reverse_button, row=7)
        self.load_csv_button = \
            generate_button(self.root, "Load CSV", self.load_csv_button, row=8)

        self.label_result, self.text_result = label_result(self.root)
    
    # Needs to be changed for final version
    def show_result(self):
        name    = self.name_entry.get()
        decade  = self.selected_decade.get()
        genre   = self.selected_movie_genre.get()
        country = self.selected_country.get()
        company = self.selected_company.get()

        # search for the movies with the given specification
        self.results = self.searcher.movie_search(\
            name, decade, genre, country, company \
        )

        self.text_result.delete('1.0', tk.END) 

        results = showable_results(self.results)
        if results is not None and len(results) > 0:
            for result in results:
                self.text_result.insert(tk.END, result)
        else: self.text_result.insert(tk.END, "No items found")

        # block text modifications
        self.text_result.config(state='disabled') 
        
    def reverse_button(self):
        #("Insert the reverse button action here")
        self.show_result()

    def load_csv_button(self):
        self.text_result.delete('1.0', tk.END) 
        proccess_csv(self.text_result)
        self.create_widgets()
        self.text_result.insert(tk.END, "CSV loaded with success!")

    def window_close(self):
        self.searcher.unload()
        self.root.destroy()

        