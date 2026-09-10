class Stock():
    def __init__(self,name,price):
        self.name=name
        self.price=price
        self.observers=[] 

    def attach(self,observer):
        self.observers.append(observer) 

    def detach(self,observer):
        self.observers.remove(observer)  

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.name, self.price)

    def set_price(self,new_price):
        self.price=new_price
        self.notify_observers()

class MobileApp:
    def update(self,name,price):
        print(f"MobileApp:{name},new price is {price}")

class EmailAlert:
    def update(self,name,price):
        print(f"EmailAlert:{name},new price is {price}")

#Main

stock1=Stock("ABC",100)

mobileapp=MobileApp()

emailalert=EmailAlert()

stock1.attach(mobileapp)

stock1.attach(emailalert)

stock1.set_price(180)

stock1.set_price(4000)

