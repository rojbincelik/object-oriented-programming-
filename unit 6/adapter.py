from abc import ABC , abstractmethod

class  PaymentProcessor (ABC):
    @abstractmethod
    def process_payment(self,amount): 
        pass

class ThirdPartyPayment: 
    def make_transaction(self, value): 
        print(f"Third-party processing payment of {value}") 

class ThirdPartyPaymentAdapter(PaymentProcessor):
    def __init__(self,third_party):
        self.third_party=third_party

    def process_payment(self, amount):
        self.third_party.make_transaction(amount)

def payment(processor,amount):

    processor.process_payment(amount)

    print("Payment Completed")

thirdpart1=ThirdPartyPayment()

adapter=ThirdPartyPaymentAdapter(thirdpart1)

payment(adapter,5000)
        