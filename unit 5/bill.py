def bill_splitter(total_bill,num_people):
    try:
        result=float(total_bill)/int(num_people)
        print(f"Each person should pay{result}")
    except ValueError:
        print("Enter a valid number")
    except ZeroDivisionError:
        print("The number of people cannot be zero")
    except:
        print("Undefined Error")
bill_splitter(500,5)
bill_splitter("abc","5")
bill_splitter(800,0)