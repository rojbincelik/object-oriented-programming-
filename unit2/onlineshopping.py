class Product:
    product_count=0
    def __init__(self,name,price):

        self.name=name
        self.price=price
        Product.product_count+=1
    def __del__(self):
        Product.product_count-=1
        print(f"product removed :{self.name}")

    @classmethod
    def total_product(cls):
        print(f"total product :{cls.product_count}")

p1=Product("melon",250)
p2=Product("milk",100)
p3=Product("tomato",30)
print(p1.name,p1.price)
print(p2.name,p2.price)
print(p3.name,p3.price)
del p2
Product.total_product()
