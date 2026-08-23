import os

if os.path.exists("balance.txt"):
    print("file exists")
    file = open("balance.txt", "r")
    content = file.read()
    file.close()
    balance = float(content)
else :
    print("file does not exists")
    balance = 5000

print("Hello User ur Balance is : " , balance)


while True:
    a = input("earn ,spend or exit : ")
    if a == "exit":
        print("good bye")
        break


    elif a == "earn" : 
        amount = float(input("how much did u  earn : "))
        balance = amount + balance
        print("ur new balance : " , balance)

        file = open("balance.txt" , "w")
        file.write(str(balance))
        file.close()

    elif a == "spend" : 
        amount = float(input("how much did u spend : "))
        balance = balance - amount 
        print("ur new balance is : " , balance)

        file = open("balance.txt", "w")
        file.write(str(balance))
        file.close()
    else : 
        print("inavalid synatax")
