class Staff:
    def __init__(self, name,email):
        self.name=name
        self.email=email
    def show_info(self):
        print(f"Name is {self.name}, Email is {self.email}")
class Lecturer(Staff):
    def __init__(self,name,email,module):
        super().__init__(name,email)
        self.module=module
class Administrater(Staff):
    def __init__(self, name, email,department):
        super().__init__(name, email)
        self.department=department
lecturer1=Lecturer("rojbin","a@gmail", "module1")
administrater1=Administrater("mehmet", "m@gmail.com","it")
lecturer1.show_info()
print(lecturer1.module)
administrater1.show_info()
print(administrater1.department)
