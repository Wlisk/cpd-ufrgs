import tkinter as tk

################# PARAMETERS #################
BACKGROUND = '#252525'                                                                                                            
FOREGROUND = 'white' 
vertical_distance = 5
horizontal_distance = 5  
widget_width = 20 
result_area_height = 32
result_area_width = 100
app_title = "Movies"  
app_size = "800x800"                                                                                                  
style = {'bg': BACKGROUND, 'fg': FOREGROUND, 'font': ('Helvetica', 12)} 
#############################################                                                          

class GraphicInterface:
    def __init__(self, root):
        self.root = root
        self.root.title(app_title)
        self.root.geometry(app_size)
        self.root.configure(bg=BACKGROUND)
        self.create_widgets()

    def create_widgets(self):
        ################# DEBUG ######################
        decades = [str(i) + "s" for i in range(1900, 2030, 10)]
        movie_genres = ["Action", "Comedy", "Drama", "Science Fiction", "Horror"]
        countries = ["Brazil","United States","Argentina", "Chile", "Colombia", "Mexico", "Spain", "Portugal"]
        companies = ["Warner Bros", "Universal Pictures", "Paramount Pictures", "20th Century Studios", "Walt Disney Pictures"]
        ##############################################
        
        tk.Label(self.root, text="Movie Title:", **style).grid(row=0, column=0, pady=vertical_distance, padx=horizontal_distance, sticky="w")
        self.name_entry = tk.Entry(self.root, **style)
        self.name_entry.grid(row=0, column=1, pady=vertical_distance, padx=horizontal_distance, sticky="ew")
        
        tk.Label(self.root, text="Release Decade:", **style).grid(row=1, column=0, pady=vertical_distance, padx=horizontal_distance, sticky="w")
        self.selected_decade = tk.StringVar(self.root, value=decades[0])
        self.decade_dropdown = tk.OptionMenu(self.root, self.selected_decade, *decades)
        self.decade_dropdown.config(width=widget_width, **style)
        self.decade_dropdown.grid(row=1, column=1, pady=vertical_distance, padx=horizontal_distance, sticky="ew")
        
        tk.Label(self.root, text="Movie Genre:", **style).grid(row=2, column=0, pady=vertical_distance, padx=horizontal_distance, sticky="w")
        self.selected_movie_genre = tk.StringVar(self.root, value=movie_genres[0])
        self.movie_genre_dropdown = tk.OptionMenu(self.root, self.selected_movie_genre, *movie_genres)
        self.movie_genre_dropdown.config(width=widget_width, **style)
        self.movie_genre_dropdown.grid(row=2, column=1, pady=vertical_distance, padx=horizontal_distance, sticky="ew")
        
        tk.Label(self.root, text="Release Country:", **style).grid(row=3, column=0, pady=vertical_distance, padx=horizontal_distance, sticky="w")
        self.selected_country = tk.StringVar(self.root, value=countries[0])
        self.country_dropdown = tk.OptionMenu(self.root, self.selected_country, *countries)
        self.country_dropdown.config(width=widget_width, **style)
        self.country_dropdown.grid(row=3, column=1, pady=vertical_distance, padx=horizontal_distance, sticky="ew")
        
        tk.Label(self.root, text="Production Company:", **style).grid(row=4, column=0, sticky="w", padx=horizontal_distance, pady=vertical_distance)
        self.selected_company = tk.StringVar(self.root)
        self.selected_company.set(companies[0]) 
        self.company_dropdown = tk.OptionMenu(self.root, self.selected_company, *companies)
        self.company_dropdown.config(width=widget_width, **style)
        self.company_dropdown.grid(row=4, column=1, padx=horizontal_distance, pady=vertical_distance, sticky="ew")
    
        self.search_button = tk.Button(self.root, text="Search", command=self.show_result)
        self.search_button.config(width=widget_width, **style)
        self.search_button.grid(row=6, column=1, padx=horizontal_distance, pady=vertical_distance)
        
        self.reverse_button = tk.Button(self.root, text="Reverse", command=self.reverse_button)
        self.reverse_button.config(width=widget_width, **style)
        self.reverse_button.grid(row=7, column=1, padx=horizontal_distance, pady=vertical_distance)
        
        self.load_csv_button = tk.Button(self.root, text="Load CSV", command=self.load_csv_button)
        self.load_csv_button.config(width=widget_width, **style)
        self.load_csv_button.grid(row=8, column=1, padx=horizontal_distance, pady=vertical_distance)
    
        self.label_result = tk.Label(self.root, text="Search result:", **style)
        self.label_result.grid(row=8, column=0, sticky="w", padx=horizontal_distance, pady=vertical_distance)
        self.text_result = tk.Text(self.root, height=result_area_height, width=result_area_width)
        self.text_result.grid(row=9, column=0, columnspan=2, padx=horizontal_distance, pady=vertical_distance)
        scrollbar = tk.Scrollbar(self.root, command=self.text_result.yview)
        scrollbar.grid(row=9, column=2, sticky='ns')
        self.text_result['yscrollcommand'] = scrollbar.set
    
    # Needs to be changed for final version
    def show_result(self):
        name = self.name_entry.get()
        decade = self.selected_decade.get()
        genre = self.selected_movie_genre.get()
        country = self.selected_country.get()
        company = self.selected_company.get()
        result = f"Movie Title: {name}\nRelease Decade: {decade}\nMovie Genre: {genre}\nRelease Country: {country}\nProduction Company: {company}" # debug line
        self.text_result.delete('1.0', tk.END) 
        self.text_result.insert(tk.END, result)
        self.text_result.config(state='disabled') 
        
    def reverse_button(self):
        print("Insert the reverse button action here")

    def load_csv_button(self):
        print("Insert the load csv button action here")
        for i in range(0,1000,1):
            result = str(i)+'\n'
            self.text_result.insert(tk.END, result)
         
    
    def configure_weights(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        for i in range(10):
            self.root.rowconfigure(i, weight=1)

root = tk.Tk()
root.resizable(False, False)
interface = GraphicInterface(root)
interface.configure_weights() 
root.mainloop()
