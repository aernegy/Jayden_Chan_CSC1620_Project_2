from tkinter import *
from tkinter import messagebox
from book import Book


class Add_Dialog(Toplevel):
    def __init__(self, parent, gen_font):
        super().__init__(parent)

        self.parent = parent
        self.gen_font = gen_font

        self.title("Add Book")
        self.geometry("300x200")
        self.resizable(width=False, height=False)

        #Make the dialog modal, i.e. the user must interact with it first
        #before returning to the parent.
        self.transient(parent)
        self.grab_set()

        self.new_book = None

        # self.gen_font = parent.gen_font

        author_label = Label(self, text="Author:", font=("Helvetica", 12))
        self.author_entry = Entry(self, font=("Helvetica", 12))
        
        title_label = Label(self, text="Title:", font=("Helvetica", 12))
        self.title_entry = Entry(self, font=("Helvetica", 12))
        
        genre_label = Label(self, text="Genre:", font=("Helvetica", 12))
        self.genre_entry = Entry(self, font=("Helvetica", 12))
        
        ok = Button(self, text="OK", command=self.on_ok, font=("Helvetica", 12))
        cancel = Button(
            self, 
            text="Cancel", 
            command=self.on_cancel, 
            font=("Helvetica", 12)
            )
        
        author_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.author_entry.grid(row=0, column=1, padx=5, pady=5)
        title_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.title_entry.grid(row=1, column=1, padx=5, pady=5)
        genre_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)
        ok.grid(row=3, column=0, pady=10)
        cancel.grid(row=3, column=1, pady=10)


        # Center the dialog relative to the parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = (parent.winfo_y() 
             + (parent.winfo_height() - self.winfo_height()) // 2
             )
        self.geometry(f"+{x}+{y}")

        self.author_entry.focus_set()


    def on_ok(self):
        author = self.author_entry.get().strip()
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()


        if not author or not title or not genre:
            messagebox.showwarning(
                "Fields cannot be empty", 
                "Please fill all fields."
                )
            
            return
        
        self.new_book = Book(author.upper(), title.upper(), genre.upper())

        self.destroy()


    def on_cancel(self):
        self.destroy()