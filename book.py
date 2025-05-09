class Book:
    """ Represents an individual book in a Library object.

    Object attributes:
    self.author -- a book's author(s).
    self.title -- a book's title.
    self.genre -- a book's genre.
    """
    
    def __init__(self, author, title, genre):
        self.author = author
        self.title = title
        self.genre = genre


    def __repr__(self):
        """ Enables duplicate-checking when adding or editing books. """
        return f"{self.title}{self.author}"