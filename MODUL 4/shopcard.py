#python have 4  collection ;
#1. list, basic collectıon
#2. tuple, like a list but imuttable(not change)
#3. set, like a list but unique (can not reply)
#4. dictionary, like a duble list you can use name and value of name together
#	Takes a list of item dictionaries 
#	Returns total cost (price × quantity for each item) 
#	Test it with at least three items. 






#sözslükler ikili ikili tutuluyor ,hem name var, 
#hem de name karsılıgı var listeler ise tek tutulur. iki farklı liste ile sözlük gibi kullanabilirsin




shopping_cart=[{"name":"milk", "price":100, "quantity":60},
               {"name":"bread", "price":10, "quantity":20},
               {"name":"sugar", "price":150, "quantity":30}]


def calculate_total(cart):
    total_cost=0
    for item in cart:

        total_cost+=item["price"]*item["quantity"]
        

    return total_cost




print (calculate_total(shopping_cart))
    

