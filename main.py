from tkinter import *
from tkinter import ttk
from library import Library
import re


class Main:
    def __init__(self):
        """
        Initialize main window with configurations, other class attributes,
        and the rest of the GUI.
        """
        self.root = Tk()
        self.root.title("Library Catalog")
        self.root.geometry("800x700")
        self.root.minsize(width=700, height=320) # Maintain GUI cleanliness.

        # Set font used throughout the GUI.
        self.gen_font = "Helvetica", 12

        # Change dialog box font.
        self.root.option_add('*Dialog.msg.font', self.gen_font)

        # Initialize class attributes. self.tree and self.search_entry
        # are defined in start_gui()
        self.tree = None
        self.search_entry = None
        self.search_value = StringVar()

        # Initialize the library object.
        self.library = Library(self)

        # To store unique tree entry IDs returned whenever inserting
        # a row into the Treeview. Used to manage programmatic
        # item selection and deletion.
        self.book_iid = []

        # Initialize the rest of the GUI.
        self.start_gui(self.root)        

        self.root.mainloop()

        # Upon closing the program, save the book records.
        self.library.save()


    def start_gui(self, root):
        # A frame to place the rest of the GUI within.
        main_window = Frame(root, relief=RIDGE)
        main_window.pack(expand=TRUE, fill=BOTH, padx=15, pady=15)

        style = ttk.Style()
        style.configure("TButton", font=self.gen_font)
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("Treeview", font=self.gen_font, rowheight=30)
        style.configure("Treeview.Heading", font=self.gen_font)

        search_label = ttk.Label(
            main_window, 
            text="Search for a title or author: ", 
            anchor="w"
            )
        
        self.search_entry = ttk.Entry(
            main_window, 
            textvariable=self.search_value,
            font=self.gen_font
            )
        
        self.tree = ttk.Treeview(
            main_window, 
            selectmode="extended", 
            show="headings",
            )
        
        #Define columns, as well as redefine #0
        self.tree["columns"] = ("author", "title", "genre")

        for column in self.tree["columns"]:
            self.tree.heading(column, text=column.capitalize(), anchor="w")
            
        self.tree.column("author", width=200, anchor="w")
        self.tree.column("title", width=200, anchor="w")
        self.tree.column("genre", width=150, anchor="w")

        self.tree_insert_handler(self.library.books)

        scrollbar = ttk.Scrollbar(main_window, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        search_button = ttk.Button(
            main_window, 
            text="Search", 
            command=lambda s=self.search_value: self.library.search(s.get())
            )
        clear_search = ttk.Button(
            main_window,
            text="Clear Search",
            command=lambda: self.library.search("")
        )
        add = ttk.Button(main_window, text="Add", command=self.library.add)
        unsel = ttk.Button(
            main_window, 
            text="Unselect", 
            command=lambda: self.sel_handler(False)
            )
        sel_all = ttk.Button(
            main_window, 
            text="Select all", 
            command=lambda: self.sel_handler(True)
            )
        delete = ttk.Button(
            main_window, 
            text="Delete", 
            command=self.library.delete,
            )


        search_label.grid(row=0, column=0, columnspan=5, sticky="w")
        self.search_entry.grid(
            row=1, 
            column=0,
            columnspan=6, 
            sticky="ew", 
            pady=10
            )
        search_button.grid(row=1, column=6, sticky="e", padx=5)
        clear_search.grid(row=1, column=7, sticky="e")
        self.tree.grid(row=2, column=0, columnspan=8, sticky="nesw")
        scrollbar.grid(row=2, column=7, sticky="nes")
        add.grid(row=3, column=0, sticky="sw", pady=10)
        unsel.grid(row=3, column=5, sticky="es", padx=5, pady=10)
        sel_all.grid(row=3, column=6, sticky="es", padx=5, pady=10)
        delete.grid(row=3, column=7, sticky="es", padx=5, pady=10)


        main_window.columnconfigure(0, weight=1)
        main_window.rowconfigure(2, weight=10)

        #Exception handling in case of the library records file
        #being empty
        try:
            self.tree.selection_set(self.book_iid[0])
        except IndexError:
            pass
        
        #Search for books after pressing return when focused on
        #the search entry
        self.search_entry.bind(
            "<Return>", 
            lambda e, s=self.search_value: self.library.search(s.get())
            )


    def tree_insert_handler(self, books):
        """
        Removes all items from self.tree and their IIDs, 
        then inserts books into self.tree while recording their IIDs.
        Handles both initialization of the system and search functionality.
        """
        self.tree.delete(*self.tree.get_children())
        self.book_iid = []

        def titlecase(text):
            return re.sub(r"[a-zA-Z]+('[a-zA-Z]+)?", 
                          lambda match: (match.group()[0].upper() 
                                         + match.group()[1:].lower()
                                         ), 
                          text
                          )
        
        for book in books:
            self.book_iid.append(
                self.tree.insert(
                    "", 
                    END, 
                    values=(
                        titlecase(book.author), 
                        titlecase(book.title), 
                        titlecase(book.genre)
                        )
                    )
                )


    def sel_handler(self, select=False):
        """
        Selects all items in self.tree if select=True, 
        otherwise deselects all items.
        """
        if select:
            self.tree.selection_set(tuple(self.tree.get_children()))

        else:
            self.tree.selection_remove(tuple(self.tree.get_children()))


Main()