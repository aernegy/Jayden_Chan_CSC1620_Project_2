from book import Book
from json import load, dump
from contextlib import chdir
from os.path import dirname
from tkinter import *
from tkinter import messagebox
from add_dialog import Add_Dialog


class Library:
    """ Represents the book library. Handles adding, deleting, and searching
    for books, displayed through the Main class.

    Public methods:
    add()
    delete() 
    search() 
    save()

    Object attributes:
    self.parent -- a call for the parent Main object.
    self.books -- a list of Book objects loaded from the JSON records,
    used to later dump into the same JSON file.
    self.file_name -- the name of the targeted JSON fie.
    """

    def __init__(self, parent):
        """ Loads the list of books from the JSON records. If the expected
        JSON file does not exist, create a new JSON file, i.e. 
        book records that has no books within.
        """

        self.parent = parent
        self.books = [] 
        self.file_name = "library_books.json"

        #########################################################
        ## Exception handling for opening the library records. ##
        #########################################################

        # To ensure that the correct directory is used for Linux
        with chdir(dirname(__file__)):
            try:
                    with open(self.file_name, "r+") as books_json:
                        for book in load(books_json):
                            self.books.append(Book(
                                book["Author"], book["Title"], book["Genre"]))

            # If the specified file of the library records does not exist,
            # create a new json file with the same name then open it.
            except FileNotFoundError as e:
                print(f"{e}. Creating new '{self.file_name}' file")
                with open(self.file_name, "w+") as books_json:
                    books_json.write("[]")
                    self.books = []


    def add(self):
        """ Allows the user to add books into the library records by
        opening a custom dialog box to allow them to enter the book
        author(s), title, and genre. Handles updating the GUI and 
        program records of Book objects and IIDs to reflect new data.
        """

        add_dialog = AddDialog(self.parent.root, self.parent.gen_font, 
                                self.books)
        
        # Forces the program to wait for add_dialog to terminate before
        # continuing.
        self.parent.root.wait_window(add_dialog)
        
        new_book = add_dialog.new_book
        
        if new_book:
            self.books.append(new_book)
            self.parent.tree_insert_handler(self.books)

            # Focuses and sets user selection to the new book.
            self.parent.tree.see(self.parent.tree.get_children()[-1])
            self.parent.tree.selection_remove(
                tuple(self.parent.tree.get_children()))
            self.parent.tree.selection_set(self.parent.tree.get_children()[-1])


    def delete(self):
        """ Handles user requests to delete selected books. Asks for user
        confirmation first before deleting the selected books. Asks user
        to select books if no books are selected.
        """

        if not self.parent.tree.selection():
            # If no books are selected:
            messagebox.showerror(title="No Books Selected", 
                                 message="Please select book(s) to delete.")
            return

        #If the user confirms their intention to delete books:
        elif messagebox.askokcancel(
                title="Delete books", 
                message="Confirm deletion of selected books?"):
            error = 0
            for book in self.parent.tree.selection():
                index = self.parent.tree.get_children().index(book)
                
                del self.books[index - error]
                error += 1

            # Update the tree with the new list of books.
            self.parent.tree_insert_handler(self.books)


    def search(self, search_value="", event=None):
        """ Handles user searches and used to clear user search values. 
        Searches for matching book authors or titles.

        Keyword parameter:
        search_value -- the search value the user wants to find in book
        authors or names. (default: '')
        event -- a dummy parameter to handle the event passed by tkinter
        binds. Does nothing. (default: None)
        """

        search_value = search_value.strip().upper()
        search_result = []

        # If the user searches for nothing/clears search results:
        if search_value == "":
            search_result = self.books

            # Delete the search value entered into the search bar.
            self.parent.search_entry.delete(0, END)
        
        else:
            for book in self.books:
                if (search_value in book.author 
                        or search_value in book.title):
                    search_result.append(book)
        
        # Updates the items in the tree with the appropriate results.
        self.parent.tree_insert_handler(search_result)


    def save(self):
        """ Handles updating the JSON records. Called whenever the GUI
        application is closed. Reformats the record of books into a list
        with multiple dictionaries since the record of books was created
        as a list of Book objects.
        """

        save_file = []

        for book in self.books:
            save_file.append(
                {
                    "Author": book.author,
                    "Title": book.title,
                    "Genre": book.genre
                }
            )

        # To ensure that the correct directory is used for Linux
        with chdir(dirname(__file__)):
            # Rewrites the entire JSON file with the latest records.
            with open(self.file_name, "w") as books_json:
                dump(save_file, books_json, indent=4)