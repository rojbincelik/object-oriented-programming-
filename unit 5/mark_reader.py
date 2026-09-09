def  read_marks(filename):
    marks=[]
    with open(filename,"r") as file:
        for line in file:
            line2=int(line)
            marks.append(line2)

    print(marks)
filename="unit 5/marks.txt"

try:
    read_marks(filename)
except FileNotFoundError:
    print(f"{filename} not found")
except ValueError:
    print(f"{filename}includes invalid data")