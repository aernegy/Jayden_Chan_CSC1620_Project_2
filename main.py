from tkinter import *
from tkinter import ttk
from library import Library
import re


class Main:
    """ A class representing the library catalog GUI. Displays data of books
    provided by a Library class.

    Public methods:
    start_gui()
    tree_insert_handler(books)
    sel_handler(select=False)

    Object attributes:
    self.root -- the GUI main window.
    self.gen_font -- the font settings used for all widgets with text.
    self.tree -- the Treeview widget used to display book data.
    self.search_entry -- the Entry widget used for entering searching values.
    self.search_value -- a StringVar() storing the search value.
    self.library -- a Library object where book data is handled.
    self.book_iid -- a list storing book IIDs from self.tree to allow for
    access and editing of items in self.tree.
    """

    def __init__(self):
        """ Defines the GUI root, class attributes, instantiates the 
        Library, and starts the root main loop. Once the main loop is exited
        upon program close, saves the changes made to data.
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
        """ Defines tkinter widgets, configures them, places them into the
        main window, adjusts the window layout, and other misc. items.
        """

        # A frame to place the rest of the GUI within.
        main_window = Frame(root)
        main_window.pack(expand=TRUE, fill=BOTH, padx=15, pady=15)  


        ################################
        ## Define widgets to be used. ##
        ################################
        search_label = ttk.Label(
            main_window, text="Search for a title or author: ", anchor="w")
        self.search_entry = ttk.Entry(
            main_window, textvariable=self.search_value, font=self.gen_font)
        
        self.tree = ttk.Treeview(
            main_window, selectmode="extended", show="headings")
        
        # Define tree columns, as well as redefine #0.
        self.tree["columns"] = ("author", "title", "genre")

        # Define the scrollbar and set it to shift tree vertically.
        scrollbar = ttk.Scrollbar(main_window, command=self.tree.yview)
        
        search_button = ttk.Button(
            main_window, text="Search", 
            command=lambda s=self.search_value: self.library.search(s.get()))
        clear_search = ttk.Button(
            main_window, text="Clear Search", 
            command=lambda: self.library.search(""))
        add = ttk.Button(main_window, text="Add", command=self.library.add)
        unsel = ttk.Button(
            main_window, text="Unselect", 
            command=lambda: self.sel_handler(False))
        sel_all = ttk.Button(
            main_window, text="Select all", 
            command=lambda: self.sel_handler(True))
        delete = ttk.Button(
            main_window, text="Delete", command=self.library.delete,)


        ################################################
        ## Edit the style & contents of widgets used. ##
        ################################################
        style = ttk.Style()
        style.configure("TButton", font=self.gen_font)
        style.configure("TLabel", font=self.gen_font)
        style.configure("Treeview", font=self.gen_font, rowheight=40)
        style.configure("Treeview.Heading", font=self.gen_font)

        # Edit the tree headings and columns.
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column.capitalize(), anchor="w")
        self.tree.column("author", width=200, anchor="w")
        self.tree.column("title", width=200, anchor="w")
        self.tree.column("genre", width=150, anchor="w")

        # Scrolling the tree vertically also moves the scrollbar.
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Insert all books into tree.
        self.tree_insert_handler(self.library.books)


        ##############################################
        ## Place all widgets and edit their layout. ##
        ##############################################
        search_label.grid(row=0, column=0, columnspan=5, sticky="w")
        self.search_entry.grid(
            row=1, column=0, columnspan=6, sticky="ew", pady=10)
        search_button.grid(row=1, column=6, sticky="e", padx=5)
        clear_search.grid(row=1, column=7, sticky="e")
        self.tree.grid(row=2, column=0, columnspan=8, sticky="nesw")
        scrollbar.grid(row=2, column=7, sticky="nes")
        add.grid(row=3, column=0, sticky="sw", pady=10)
        unsel.grid(row=3, column=5, sticky="es", padx=5, pady=10)
        sel_all.grid(row=3, column=6, sticky="es", padx=5, pady=10)
        delete.grid(row=3, column=7, sticky="es", padx=5, pady=10)

        # Ensure tree and search_entry expand horizontally
        # upon window resizing.
        main_window.columnconfigure(0, weight=1)

        # Ensure the tree expands vertically upon window resizing.
        main_window.rowconfigure(2, weight=1)


        #####################
        ## Misc. measures. ##
        #####################

        # Automatically sets user selection to be the first item in tree
        # upon program start. Exception handling used in case that the 
        # records file is empty.
        try:
            self.tree.selection_set(self.book_iid[0])
        except IndexError:
            pass
        
        # Search for books after pressing return when the keyboard
        # is focused on search_entry.
        self.search_entry.bind(
            "<Return>", 
            lambda e, s=self.search_value: self.library.search(s.get())
            )


    def tree_insert_handler(self, books):
        """ Handles editing items in tree upon adding, deleting, 
        initializing, and searching books.

        Removes all items from self.tree and their IIDs, 
        then inserts books into self.tree while recording their IIDs.

        Keyword parameters:
        books -- the list of Book objects to load onto the tree. (required)
        """

        # Deletes all items in tree and book_iid.
        self.tree.delete(*self.tree.get_children())
        self.book_iid = []        
        
        # Insert books into the tree while appending their iid into
        # book_iid.
        for book in books:
            self.book_iid.append(
                self.tree.insert(
                    "", END, 
                    values=(self.titlecase(book.author), 
                            self.titlecase(book.title), 
                            self.titlecase(book.genre))))


    def sel_handler(self, select=False):
        """ Selects all items in self.tree if select=True, otherwise 
        deselects all items.

        Keyword parameters:
        select -- Selects all items if True, unselects all items otherwise
        (default: False).
        """

        if select:
            self.tree.selection_set(tuple(self.tree.get_children()))

        else:
            self.tree.selection_remove(tuple(self.tree.get_children()))


    @staticmethod
    def titlecase(text):
        """ A function to better convert text to title case than .title().
        Handles apostrophes (e.g. 's) better than .title().

        Keyword parameters:
        text -- the text to convert to title case. (required)

        Explanation:
        re.sub(pattern, substitute, input_text): Looks for pattern in 
        input_text and replaces the pattern in input_text with 
        substitute.
        
        r"[a-zA-Z]+('[a-zA-Z]+)?": A pattern in input_text that looks
        like "{letters}'{more letters}".
        
        match: an object representing a pattern found in input_text.
        match.group(): returns a string of the pattern found.
        
        match.group()[0].upper() + match.group()[1:].lower(): ensures
        the first character of each pattern is capital while the rest
        of the characters are lowercase
        """
        
        return re.sub(r"[a-zA-Z]+('[a-zA-Z]+)?", 
                        lambda match: (match.group()[0].upper() 
                                        + match.group()[1:].lower()), 
                        text)


Main()