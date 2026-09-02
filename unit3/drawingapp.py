from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
class Rectangle(Shape):
    def __init__(self,length,width):
        self.length=length
        self.width=width
    def area(self):
        total=self.length*self.width
        return total
class Circle(Shape):
    def __init__(self,radius):
        self.radius=radius
    def area(self):
        total=3.14*self.radius*self.radius
        return total
shapes=[
    Rectangle(34,45),Circle(90),Rectangle(56,78),Circle(78)   
]
for i in shapes:
    print(i.area())

