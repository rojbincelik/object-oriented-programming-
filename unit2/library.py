class Book:
    
    
    
    def __init__(self,title, author ,  year):
        self.title=title
        self.author=author
        self.year=year
    def details (self):
        print(f"Title={self.title}\nAuthor={self.author}\nYear{self.year}")


crime_book=Book("Murder on the Orient Express", "Agatha Christe", 1934)

romance_book=Book("Pride and Prejudice", "Jane Austen",1813) 

drama_book=Book ("The Fault in Our Stars", "John Green ", 2012)


crime_book.details()
romance_book.details()
drama_book.details()
