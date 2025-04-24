from book import Book
from json import load, dump
from contextlib import chdir
from os.path import dirname
from tkinter import *
from tkinter import messagebox
from add_dialog import AddDialog


class Library:
    """ Represents the book library. Handles adding, deleting, and searching
    for books, displayed through the Main class.

    Public methods:
    add()
    delete() 
    search(search_value='', event=None) 
    save()
    edit(index, iid)

    Object attributes:
    self.parent -- a call for the parent Main object.
    self.books -- a list of Book objects loaded from the JSON records,
    used to later dump into the same JSON file. Maintained to be parallel
    with main.py's book_iid list, such that a book object of an index in 
    books has the same index in book_iid.
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
            # create a new JSON file with the same name then open it.
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
        
        # If a book was added, add its details and IID to the corresponding
        # lists, then focus on it in the tree and save the changes.
        if new_book:
            self.books.append(new_book)
            self.parent.book_iid.append(
                self.parent.tree.insert(
                    "", END, values=(
                        self.parent.titlecase(new_book.author), 
                        self.parent.titlecase(new_book.title), 
                        self.parent.titlecase(new_book.genre))))

            # Focuses and sets user selection to the new book, then saves.
            self.parent.tree.see(self.parent.tree.get_children()[-1])
            self.parent.tree.selection_remove(
                tuple(self.parent.tree.get_children()))
            self.parent.tree.selection_set(self.parent.tree.get_children()[-1])
            self.save()


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
            # Identify each book's index in book_iid and self.books
            # using its IID. Then remove it from the tree widget and lists.
            for book in self.parent.tree.selection():
                index = self.parent.book_iid.index(book)
                self.parent.tree.delete(book)
                del self.parent.book_iid[index]
                del self.books[index]

            self.save()


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

        # Used to store the index of search results 
        # in book_iid and self.books.
        search_result = []

        # If the user searches for nothing/clears search results:
        if search_value == "":
            search_result = range(len(self.books))

            # Delete the search value entered into the search bar.
            self.parent.search_entry.delete(0, END)
        
        else:
            for book in self.books:
                if (search_value in book.author 
                        or search_value in book.title):
                    search_result.append(self.books.index(book))
        
        # Temporarily removes all items from the tree widget.
        for item in self.parent.tree.get_children():
            self.parent.tree.detach(item)

        if not search_result:
            messagebox.showinfo(title="Empty Search Results",
                                message="No search results found.")

        # Reattaches the search results to the tree widget.
        for book in search_result:
            self.parent.tree.move(self.parent.book_iid[book], "", END)


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


    def edit(self, index, iid):
        """ Handles the logic behind editing functionality. Calls a dialog
        box to enable users to edit book details. Then, updates the details
        in self.books, the tree widget, and the JSON records.

        Keyword parameters:
        index -- the index of the selected item in book_iid and self.books 
        (required).
        iid -- the IID of the selected item in the tree widget (required).
        """

        add_dialog = AddDialog(self.parent.root, self.parent.gen_font, 
                               self.books, index, iid, edit=True)
        
        # Forces the program to wait for add_dialog to terminate before
        # continuing.
        self.parent.root.wait_window(add_dialog)

        new_book = add_dialog.new_book

        if new_book:
            self.books[index].author = new_book.author
            self.books[index].title = new_book.title
            self.books[index].genre = new_book.genre

            # Edits the details in the tree widget.
            self.parent.tree.item(
                iid, values=(
                    self.parent.titlecase(new_book.author), 
                    self.parent.titlecase(new_book.title), 
                    self.parent.titlecase(new_book.genre)))

            # Focuses and sets user selection to the new book, then saves.
            self.parent.tree.see(iid)
            self.parent.tree.selection_remove(
                tuple(self.parent.tree.selection()))
            self.parent.tree.selection_set(iid)
            self.save()