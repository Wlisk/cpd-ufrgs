# type imports 
from tkinter import END
# module imports
from tkinter.filedialog import askopenfilename
from scripts.binaries.binaries import generate_binaries
# const imports 
from scripts.config import DATASETS_DIR

def proccess_csv(self):
    filetypes = [('csv files', '*.csv')] 

    filename = askopenfilename( \
        title='Load a CSV File', \
        initialdir=DATASETS_DIR, \
        filetypes=filetypes \
    )

    generate_binaries(filename)

    

