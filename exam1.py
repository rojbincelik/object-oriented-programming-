class Animal:
    def __init__(self,spice:str,name:str ,age:int,):
        self.age=age
        self.name=name
        self.spice=spice
    def voice(self):
        return ""
    def move(self):
        return ""
    def introduce(self ):
        return f"Hello I am {self.spice}, my name is {self.name}, and I am {self.age} years old."
class Fish(Animal):
    def move (self):
        return " I can swim"
class Dog(Animal):
    def move(self): 
        return "I can walk"
    def voice(self):
        return " hav hav " 
    def fetch(self, object):
        
        return f"if you throw any {object} I can bring it back "
class Bird(Animal):
    def move(self):
        return "I believe I can fly"
    def voice(self):
        return " cik cik"
dove=Bird("dove", "rose",1)
print(dove.introduce())
print(dove.move())
print(dove.voice())

sea_bass=Fish("seabass","rojbin",7)
print(sea_bass.introduce())
kangal=Dog("kangal","eyo",3)
print(kangal.introduce())


