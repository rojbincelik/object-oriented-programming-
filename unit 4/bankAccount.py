class BankAccount:
    def __init__(self,owner):
        self.owner=owner
        self.__balance=0
    def deposit(self,amount):
        
        if amount>0:
            self.__balance+=amount
            print("Balance updated")
        else:
            print(" You can not deposite negative amount")
    def withdraw(self,amount):
        if amount<0:
            print(" You can not withdraw negative amount")
        elif amount>self.__balance:
            print(" You can not  withdraw more than your balance allows")
        else:
            self.__balance-=amount
            print(f"You have {self.__balance} in your account")
    def get_balance(self):
        return self.__balance
bankaccount1=BankAccount("Ogun")
bankaccount1.__balance=100
print(bankaccount1.get_balance())
bankaccount1.deposit(900000000)
bankaccount1.withdraw(8000000)
print(bankaccount1.get_balance())

