class Patient:
    def __init__(self,name,age,medical_history=[]):
        self.name=name
        self._age=age
        self.__medical_history=medical_history
    def get_medical_summary(self):
       
        print(f"Patient name is {self.name}")
        print("Sensitive medical history hidden")
    def add_medical_note(self,note):
        self.__medical_history.append(note)
        print("Medical history updated")
patient1=Patient("Ogun",30)
#print(patient1.__medical_history)
patient1.add_medical_note("He uses mounjurna")
patient1.get_medical_summary()




