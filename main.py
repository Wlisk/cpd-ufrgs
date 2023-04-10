#!/usr/bin/python
# type imports
from scripts.graphics.GUI import GraphicInterface
from tkinter import Tk

from scripts.config import CSVFILE
from scripts.binaries.binaries import generate_binaries

def main():
    generate_binaries(CSVFILE)

    root = Tk()
    root.resizable(False, False)
    interface = GraphicInterface(root)
    interface.configure_weights() 
    root.protocol("WM_DELETE_WINDOW", interface.window_close)
    root.mainloop()

if __name__ == "__main__":
    main()

