inventory = int(0)
totalstock = int(0)
rejectcounter = int(0)
quit = ""

print("Welcome to the Inventory Auditor!")
print("Please enter the number of stock quantity:")

while quit != "quit":
    userinput = input()
    if userinput == "quit":
        print("Exiting the Inventory Auditor. Total unit processed:", totalstock, "and Number of rejected entries:", rejectcounter)
        break
    elif userinput.isdigit():
        newstock = int(userinput)
        totalstock += newstock
        inventory += newstock
        if inventory > 500:
            print("Inventory limit exceeded. exiting the program.")
            break
        else:
            print("Total stock entries entered:", totalstock, "Please enter the next stock quantity or type 'quit' to exit.")
    else:
        rejectcounter += 1
        print("Invalid input. Please enter a valid number or type 'quit' to exit.")
    