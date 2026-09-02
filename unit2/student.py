class Student:
    count=0
    def __init__(self,name,grade):
        Student.count+=1
        self.name=name
        self.grade=grade


    @classmethod
    def show_count(st):
        print(f"Total student: {st.count}")



student1=Student("rojbin",100)
student2=Student("neriman",50)
student3=Student("mehmet",99)

Student.show_count()