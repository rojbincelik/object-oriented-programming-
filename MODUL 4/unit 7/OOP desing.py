# bad_todo.py 




class Task:
    def __init__(self,name,done=False):
        self.name=name
        self.done=done

    def mark_done(self):
        self.done=True

class TodoList:
    def __init__(self):
        self.tasks=list()

    def add_task(self,name):
        self.tasks.append(Task(name))

    def mark_done(self,index):
        self.tasks[index].mark_done()

    def show_tasks(self):
        for t in self.tasks: 
            status = "✓" if t.done else "✗" 
            print(status, t.name) 

#main
if __name__=="__main__":
    manager=TodoList()
    manager.add_task("Buy milk") 
    manager.add_task("Finish assignment")  
    manager.mark_done(0) 
    manager.show_tasks() 


        