# type imports
from tkinter import Tk, Button
from typing import Callable
# const imports
from scripts.graphics.controls import \
    VERTICAL_DISTANCE, HORIZONTAL_DISTANCE, WIDGET_WIDTH, STYLE

# generate a button for the window
def generate_button(root: Tk, name: str, fn: Callable, row: int) -> Button:
    button = Button(root, text=name, command=fn)
    button.config(width=WIDGET_WIDTH, **STYLE)
    button.grid(row=row, column=1, padx=HORIZONTAL_DISTANCE, pady=VERTICAL_DISTANCE)
    return button
