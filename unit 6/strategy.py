class DiscountStrategy:
    def apply(self,price):
        pass

class NoDiscount(DiscountStrategy):
    def apply(self,price):
        return price

class PercentageDiscount(DiscountStrategy):
    def __init__(self,percantage):
        self.percantage=percantage

    def apply(self, price):
        return (price-price*self.percantage/100)

class FixedDiscount(DiscountStrategy):
    def __init__(self,amount):
        self.amount=amount

    def apply(self, price):
        return (price-self.amount)


class Checkout:
    def __init__(self,discount_strategy):
        self.discount_strategy=discount_strategy

    def final_price(self,original_price):
        return self.discount_strategy.apply(original_price)

#Main

checkout1=Checkout(NoDiscount())

checkout2=Checkout(PercentageDiscount(20))

checkout3=Checkout(FixedDiscount(5))

print(checkout1.final_price(100))

print(checkout2.final_price(100))

print(checkout3.final_price(100))





    

        
    
