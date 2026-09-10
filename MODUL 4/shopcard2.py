class CartItem():
    def __init__(self,name,price,quantity):
        self.name=name
        self.price=price
        self.quantity=quantity
class ShoppingCart():
    def __init__(self):
        self.items=[]
    def add_item(self,item):
        self.items.append(item)
    def calculate_total(self):
        total_cost=0
        for item in self.items:
            total_cost+=item.price*item.quantity
        return total_cost
        
shopping_cart=ShoppingCart()
shopping_cart.add_item(CartItem("milk",100,150))
shopping_cart.add_item(CartItem("bread",10,10))
shopping_cart.add_item(CartItem("sugar",190,19))
print (shopping_cart.calculate_total())