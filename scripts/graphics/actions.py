# type imports 
from tkinter import Text, END
# module imports
from tkinter.filedialog import askopenfilename
from scripts.binaries.binaries import generate_binaries
# const imports 
from scripts.config import DATASETS_DIR

def proccess_csv(text: Text):
    filetypes = [('csv files', '*.csv')] 

    filename = askopenfilename( \
        title='Load a CSV File', \
        initialdir=DATASETS_DIR, \
        filetypes=filetypes \
    )

    text.insert(END, "CSV loading...")

    generate_binaries(filename)

