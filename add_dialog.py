from tkinter import *
from tkinter import messagebox, ttk
from book import Book


class AddDialog(Toplevel):
    """ Handles the custom dialog box generated to handle user input for
    adding a new book and editing book details, and sends the input data 
    to a Library object. Inherits from tkinter.Toplevel.

    Public methods:
    on_ok()
    on_cancel()

    Object attributes:
    self.new_book -- stores the new book's data in a dictionary.
    self.books -- a call for the parent Library object's list of book
    objects called the same name.
    self.edit -- stores the mode in which the object was instantiated for.
    self.author/self.title_var/self.genre -- Stores the values inputted
    into the corresponding entry widgets.
    """

    def __init__(self, parent, gen_font, books, index=0, iid="", edit=False):
        """ Creates the custom dialog box using tkinter's Toplevel object.
        Defines the widets used, places them into the dialog box, and other
        items.

        Keyword parameters:
        parent -- a call for the tkinter root to pass into the __init__
        of the Toplevel parent. (required)
        gen_font -- a call for the font style used in main.py. (required)
        books -- a call for the parent Library object's list of book
        objects called the same name. (required)
        index -- the index of the book being edited. Used if AddDialog 
        is instantiated for editing. (default: 0)
        iid -- the treeview IID of the book being edited. Used if AddDialog
        is instantiated for editing. (default: '')
        edit -- a boolean value to determine whether to enable editing
        features. (default: False)
        """

        # Call the __init__ function of Toplevel, passing Main as the root.
        super().__init__(parent)

        self.new_book = None
        self.books = books
        self.edit = edit
        self.author = StringVar()
        self.title_var = StringVar()
        self.genre = StringVar()

        # If in editing mode, set the default values of the entry widgets
        # to be the details of the book being edited. Also set the window
        # title appropriately.
        if self.edit:
            self.author.set(self.books[index].author)
            self.title_var.set(self.books[index].title)
            self.genre.set(self.books[index].genre)
            self.title("Edit Book")
        
        else:
            self.title("Add Book")
        
        self.geometry("500x160")
        self.resizable(width=False, height=False)

        # Gets tkinter to create the window before continuing.
        self.update_idletasks()


        ################################
        ## Define widgets to be used. ##
        ################################
        author_label = ttk.Label(self, text="Author:")
        author_entry = Entry(self, font=gen_font, textvariable=self.author)
        title_label = ttk.Label(self, text="Title:")
        title_entry = Entry(self, font=gen_font, textvariable=self.title_var)
        genre_label = ttk.Label(self, text="Genre:")
        genre_entry = Entry(self, font=gen_font, textvariable=self.genre)
        ok = ttk.Button(self, text="OK", command=self.on_ok)
        cancel = ttk.Button(self, text="Cancel", command=self.on_cancel)
        

        ###########################################
        ## Place all widgets and configure them. ##
        ###########################################
        author_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")
        author_entry.grid(row=0, column=1, padx=15, pady=5, sticky="ew")
        title_label.grid(row=1, column=0, padx=15, pady=5, sticky="w")
        title_entry.grid(row=1, column=1, padx=15, pady=5, sticky="ew")
        genre_label.grid(row=2, column=0, padx=15, pady=5, sticky="w")
        genre_entry.grid(row=2, column=1, padx=15, pady=5, sticky="ew")
        ok.grid(row=3, column=0, padx=15, pady=15, sticky="nw")
        cancel.grid(row=3, column=1, padx=15, pady=15, sticky="ne")

        self.columnconfigure(1, weight=1)

        #####################
        ## Misc. measures. ##
        #####################

        # Gets tkinter to place all widgets before continuing.
        self.update_idletasks()

        # Calculates x and y-coordinates needed to be placed on in order
        # to be centered on the main GUI.
        x = (parent.winfo_x() 
             + (parent.winfo_width() - self.winfo_width()) // 2)
        y = (parent.winfo_y() 
             + (parent.winfo_height() - self.winfo_height()) // 2)
        
        # Set window position according to calculated coordinates.
        self.geometry(f"+{x}+{y}")

        # Make the dialog modal, i.e. the user must interact with it first
        # before returning to the parent.
        self.transient(parent)
        self.grab_set()

        # Set initial keyboard focus to be on author_entry.
        author_entry.focus_set()


    def on_ok(self):
        """ Handles the logic upon the user submitting their inputs.
        Ensures that user input is not empty upon submission and that 
        the added book does not have a duplicate title as an existing
        book in the database. Allows user to cancel the process. 
        """

        # .get() required to retrieve user input in each entry as a string*.
        author = self.author.get().strip()
        title = self.title_var.get().strip()
        genre = self.genre.get().strip()

        # If any entry is empty:
        if not author or not title or not genre:
            messagebox.showwarning("Fields cannot be empty", 
                                   "Please fill all fields.", parent=self)
            
            # Does not close the dialog box.
            return
        
        self.new_book = Book(author.upper(), title.upper(), genre.upper())
        
        # If new_book's title and author is the same with an existing book
        # and the dialog is not open for editing a book:
        if (repr(self.new_book) in [repr(book) for book in self.books] 
                and not self.edit):
            messagebox.showwarning("Duplicate detected", 
                                   "This book has already been added.",
                                   parent=self)

            # Does not close the dialog box.
            return
        
        # Close the dialog box.
        self.destroy()


    def on_cancel(self):
        """ Closes the dialog box when the user presses 'cancel'. 
        Ensures the object returns void.
        """

        self.new_book = None
        self.destroy()