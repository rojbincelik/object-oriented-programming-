def log_message(filename, message):

    try:
        with open(filename,"a") as file:
            file.write(message+"\n")
            print("MESSAGE IS WRİTTEN") 
    except IOError:
        print("INPUT/OUTPUT ERROR")
    except Exception as e:
        print(f"error:{e}")
    finally:
        print("Finished log attempt")

log_message("log.txt","system error")
  
