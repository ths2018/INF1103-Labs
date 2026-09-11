inventory = int(0)
totalstock = int(0)
quit = ""

while quit != "quit":
    print("Welcome to the Inventory Auditor!")
    print("Please enter the number of stock quantity:")
    newstock = input()
    if newstock != "quit" and newstock.isdigit():
        newstock = int(newstock)
        totalstock += newstock
        print("Current inventory:", inventory)
        print("Total stock entries:", totalstock, f"Please enter the next stock quantity or type 'quit' to exit.")
    elif newstock != "quit" and not newstock.isdigit():
        print("Invalid input. Please enter a valid number or type 'quit' to exit.")
    elif newstock == "quit":
        break