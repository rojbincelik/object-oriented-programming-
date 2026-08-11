class Book:
    def __init__(self, title, author , isbn, availability):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.availability=availability
    def borrow(self):
        if self.availability==True:
            print(f"please bring back to {self.title} in 14 days ")
            self.availability=False
        else: 
            print(f"you can not borrow {self.title}")

    def return_book(self):
        if self.availability==False:
            print(f"{self.title} Book returned successfully")
            self.availability=True
        else: 
            print(f"{self.title} the book was still there")

    def display_info(self):
        status = "Available" if self.availability else "Not Available"
        print(f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {status}")

    # Adding books to the library

book1 = Book("1984", "George Orwell", "9780451524935", False)
book2 = Book("To Kill a Mockingbird", "Harper Lee", "9780060935467", True)

                    
# Display initial book information

book1.display_info()
book2.display_info()
                        
# Borrowing a book

book2.borrow()
book2.display_info()
                        
# Trying to borrow the same book again

book2.borrow()
    
# Returning the book

book1.return_book()
book1.display_info()