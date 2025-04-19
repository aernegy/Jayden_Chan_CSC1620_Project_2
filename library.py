from book import Book
from json import load, dump
from contextlib import chdir
from os.path import dirname
from tkinter import *
from tkinter import messagebox
from add_dialog import Add_Dialog


class Library:
    def __init__(self, parent):
        self.parent = parent

        self.books = [] 

        #Exception handling for opening the library records.
        #If the specified file name of the library records does not exist,
        #create a new json file with the same name then open it.
        self.file_name = "library_books.json"
        try:
            #To ensure that the correct directory is used for Linux
            with chdir(dirname(__file__)):
                with open(self.file_name, "r+") as books_json:
                    for book in load(books_json):
                        self.books.append(
                            Book(book["Author"], book["Title"], book["Genre"])
                            )

        except FileNotFoundError:
            print("ERROR: File not found. Creating new file")
            with open(self.file_name, "w+") as books_json:
                books_json.write("[]")
                self.books = []


    def add(self):
        add_dialog = Add_Dialog(self.parent.root, self.parent.gen_font)
        self.parent.root.wait_window(add_dialog)
        new_book = add_dialog.new_book
        
        if new_book:
            self.books.append(new_book)
            self.parent.tree_insert_handler(self.books)
            

            self.parent.tree.see(self.parent.book_iid[-1])
            self.parent.tree.selection_remove(
                tuple(self.parent.tree.get_children())
                )
            self.parent.tree.selection_set(self.parent.book_iid[-1])


    def delete(self):
        if not self.parent.tree.selection():
            messagebox.showerror(
                title="No Books Selected", 
                message="Please select book(s) to delete."
                )
            return
            
        if messagebox.askokcancel(
            title="Delete books", 
            message="Confirm deletion of selected books?"
            ):

            for book in self.parent.tree.selection():
                self.parent.book_iid.remove(book)
                del self.books[self.parent.tree.selection().index(book)]
                self.parent.tree.delete(book)


    def search(self, search_value="", event=None):
        search_value = search_value.strip().upper()
        search_result = []

        if search_value == "":
            search_result = self.books
            self.parent.search_entry.delete(0, END)
        
        else:
            for book in self.books:
                if (search_value in book.author 
                        or search_value in book.title):
                    search_result.append(book)
        
        self.parent.tree_insert_handler(search_result)


    def save(self):
        save_file = []

        for book in self.books:
            save_file.append(
                {
                    "Author": book.author,
                    "Title": book.title,
                    "Genre": book.genre
                }
            )

        with open(self.file_name, "w") as books_json:
            dump(save_file, books_json, indent=4)