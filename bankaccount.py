class BankAccount:
    def __init__(self,name):
        self.name=name
        self.balance=0
        print(f"Account created for {self.name}")
    
    def __del__(self):
        print(f"Account closed for {self.name}")


bankaccount1=BankAccount( "Rojbin")
del bankaccount1