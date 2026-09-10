from abc import ABC,abstractmethod
class Notification(ABC):
    @abstractmethod
    def send(self,message):
        pass

class EmailNotification(Notification):
    def send(self,message):
        print(f"EMAİL:{message}")

class SMSNotification(Notification):
    def send(self,message):
        print(f"SMS:{message}")

class NotificationFactory():
    @classmethod
    def create_notification(cls,type_name):
        if type_name=="email":
            return EmailNotification()
        if type_name=="sms":
            return SMSNotification() 
        raise ValueError(" UNKNOWN TYPE ")
def main():
    message1=NotificationFactory.create_notification("email")
    message2=NotificationFactory.create_notification("sms")
    message1.send("rojbincelik@karakochukuk.com")
    message2.send("Hello")

main()