from abc import ABC,abstractmethod
class TaskCollection(ABC):
    @abstractmethod
    def add_task(self,task):
        pass
    @abstractmethod
    def get_next_task(self):
        pass
    @abstractmethod
    def has_tasks(self):
        pass
class TaskQueue(TaskCollection):
    def __init__(self):
        self.tasks=[]
    def add_task(self, task):
        self.tasks.append(task)
    def get_next_task(self):
        if self.tasks:
            x=self.tasks.pop(0)
            print(x)
        else:
            print("You complete all your tasks")
    def has_tasks(self):
        if self.tasks:
            return True
        return False
class TaskStack(TaskCollection):
    def __init__(self):
        self.tasks=[]
    def add_task(self, task):
        self.tasks.append(task)
    def get_next_task(self):
        if self.tasks:
            x=self.tasks.pop()
            print(x)
        else:
            print("You complete all your tasks")
    def has_tasks(self):
        if self.tasks:
            return True
        return False
taskQ=TaskQueue()
taskS=TaskStack()
taskQ.add_task("Task A")
taskQ.add_task("Task B")
taskQ.add_task("Task c")
taskS.add_task("Task A")
taskS.add_task("Task B")
taskS.add_task("Task c")
taskQ.get_next_task()
taskQ.get_next_task()
taskQ.get_next_task()
taskQ.get_next_task()
taskS.get_next_task()
taskS.get_next_task()
taskS.get_next_task()
taskS.get_next_task()
