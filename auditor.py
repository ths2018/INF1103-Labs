inventory = int(0)
totalstock = int(0)
quit = ""

while quit != "quit":
    print("Welcome to the Inventory Auditor!")
    print("Please enter the number of stock quantity:")
    newstock = input()
    if newstock == "quit":
        break