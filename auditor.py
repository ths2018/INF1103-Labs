inventory = int(0)
totalstock = int(0)
rejectcounter = int(0)
quit = ""

print("Welcome to the Inventory Auditor!")
print("Please enter the number of stock quantity:")

while quit != "quit":
    newstock = input()
    if newstock != "quit" and newstock.isdigit():
        newstock = int(newstock)
        totalstock += newstock
        print("Total stock entries entered:", totalstock, "Please enter the next stock quantity or type 'quit' to exit.")
    elif newstock != "quit" and not newstock.isdigit():
        rejectcounter += 1
        print("Invalid input. Please enter a valid number or type 'quit' to exit.")
    elif newstock == "quit":
        print("Exiting the Inventory Auditor. Total unit processed:", inventory+totalstock, "and Number of rejected entries:", rejectcounter)
        break