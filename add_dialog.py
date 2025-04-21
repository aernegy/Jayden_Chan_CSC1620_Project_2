from tkinter import *
from tkinter import messagebox
from book import Book


class AddDialog(Toplevel):
    """ Handles the custom dialog box generated to handle user input for
    adding a new book and sends the input data to a Library object. Inherits
    from tkinter.Toplevel.

    Public methods:
    on_ok()
    on_cancel()

    Object attributes:
    self.parent -- a call for the parent Main object.
    self.new_book -- stores the new book's data in a dictionary.
    self.books -- a call for the parent Library object's list of book
    objects called the same name.
    """

    def __init__(self, parent, gen_font, books):
        """ Creates the custom dialog box using tkinter's Toplevel object.
        Defines the widets used, places them into the dialog box, and other
        items.
        """

        # Call the __init__ function of Toplevel, passing Main as the root.
        super().__init__(parent)

        self.parent = parent
        self.new_book = None
        self.books = books
        self.author = StringVar()
        self.title_var = StringVar()
        self.genre = StringVar()

        self.title("Add Book")
        self.geometry("300x200")
        self.resizable(width=False, height=False)

        #Make the dialog modal, i.e. the user must interact with it first
        #before returning to the parent.
        self.transient(parent)
        self.grab_set()


        ################################
        ## Define widgets to be used. ##
        ################################
        author_label = Label(self, text="Author:", font=gen_font)
        author_entry = Entry(self, font=gen_font, textvariable=self.author)
        title_label = Label(self, text="Title:", font=gen_font)
        title_entry = Entry(self, font=gen_font, textvariable=self.title_var)
        genre_label = Label(self, text="Genre:", font=gen_font)
        genre_entry = Entry(self, font=gen_font, textvariable=self.genre)
        ok = Button(self, text="OK", command=self.on_ok, font=gen_font)
        cancel = Button(self, text="Cancel", command=self.on_cancel, 
                        font=gen_font)
        

        ########################
        ## Place all widgets. ##
        ########################
        author_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        author_entry.grid(row=0, column=1, padx=5, pady=5)
        title_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        title_entry.grid(row=1, column=1, padx=5, pady=5)
        genre_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        genre_entry.grid(row=2, column=1, padx=5, pady=5)
        ok.grid(row=3, column=0, padx=5, pady=10, sticky="w")
        cancel.grid(row=3, column=1, padx=5, pady=10, sticky="e")


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
                                   "Please fill all fields.")
            
            # Does not close the dialog box.
            return
        
        self.new_book = Book(author.upper(), title.upper(), genre.upper())
        
        # If new_book's title is the same with an existing book:
        if repr(self.new_book) in [repr(book) for book in self.books]:
            messagebox.showwarning("Duplicate detected", 
                                   "This book has already been added.")

            # Does not close the dialog box.
            return
        
        # Close the dialog box.
        self.destroy()


    def on_cancel(self):
        """ Closes the dialog box when the user presses 'cancel'."""
        self.destroy()