from abc import abstractmethod,ABC
class PaymentMethod(ABC): 
    @abstractmethod
    def pay (self, amount):
        pass
class CardPayment(PaymentMethod):
    def __init__(self, card_number):
        self.card_number=card_number
    def pay (self, amount):
        print(f"Paid {amount} using card ending with {self.card_number[-4:]}" )
class PayPalPayment(PaymentMethod):
    def __init__(self, email):
            self.email=email
    def pay (self, amount):
         print(f"Paid {amount} using card ending with {self.email}" )
paymentmethods=[CardPayment("090876"),PayPalPayment("a@gmail.cok")]
for i in paymentmethods:
     i.pay(50)

    
