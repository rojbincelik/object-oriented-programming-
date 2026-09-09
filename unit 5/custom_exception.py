class InsufficientFundsError(Exception):
    """ Not enough money in the account"""
    pass

class BankAccount:
    def __init__(self,balance):
        self.__balance=balance

    def deposit(self,amount):
        self.__balance+=amount
        print(f"withdraw:{amount}\nbalance:{self.__balance}")      
        
    def withdraw(self,amount):
        if amount>self.__balance:
            raise InsufficientFundsError("Not enough money in the account")

        else:
            self.__balance-=amount  
            print(f"withdraw:{amount}\nbalance:{self.__balance}") 

bankaccount=BankAccount(10_000)
bankaccount.deposit(50_000)

try:
    bankaccount.withdraw(70_000)
except InsufficientFundsError as error:
    print(error)

