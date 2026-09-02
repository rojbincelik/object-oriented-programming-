class Vehicle:
    def __init__(self,base_fare):
        self.base_fare=base_fare    
    def calculate_fare(self,distance):
        return self.base_fare*distance
class Bus(Vehicle):
    pass
class Taxi(Vehicle):
    def __init__(self, base_fare,base_fee):
        super().__init__(base_fare)
        self.base_fee=base_fee
    def calculate_fare(self, distance):
        return super().calculate_fare(distance)+self.base_fee
bus1=Bus(30)
taxi1=Taxi(40,20)


vehicles=[bus1,taxi1]
for i in vehicles:
    total=i.calculate_fare(10)
    
    print(total)