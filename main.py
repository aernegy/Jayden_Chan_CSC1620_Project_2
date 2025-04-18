from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Main:
    def __init__(self):
        root = Tk()
        root.title("Library Catalog")
        root.geometry("500x400")

        self.start_gui(root)        

        root.mainloop()


    def start_gui(self, root):
        main_window = Frame(root)
        main_window.pack(expand=TRUE)

        search_label = Label(main_window, text="Search for a title or author: ", anchor="w")
        search_label.grid(row=0, column=0, sticky="w")

        search_value = StringVar()
        search_entry = ttk.Entry(root, textvariable=search_value)
        search_entry.grid(row=1, column=0, sticky="ew", padx=20)

        root.columnconfigure(0, weight=1)

Main()