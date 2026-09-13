from models import Student
from services import add_student , find_student

students=[]

student1 = Student(404,"Rojbin")
student2 = Student(1001,"Ogün")

add_student(students , student1)
add_student(students , student2)

search=find_student(students , 1001)
print(search.name)