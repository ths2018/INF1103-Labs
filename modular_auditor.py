inventory = int(0)
rejectcounter = int(0)

def get_valid_input(user):
    if user.lower() == "quit":
        return None
    elif user.isdigit():
        return True
    else:
        return False

def process_delivery(current_stock, new_stock):
    current_stock += new_stock
    return current_stock

def calculate_tax(amount):
    tax_rate = 0.10  # Example tax rate of 10%
    tax_amount = amount * tax_rate
    return tax_amount

def generate_report(total_stock, rejected_entries):
    report = f"Inventory Report:\nTotal Stock: {total_stock}\nRejected Entries: {rejected_entries}"
    return report

print("Welcome to the Inventory Auditor!")
print("Please enter the number of stock quantity:")

while True:
    userinput = input()
    if get_valid_input(userinput) is None:
        print(generate_report(inventory, rejectcounter))
        break
    elif get_valid_input(userinput) is True:
        newstock = int(userinput)
        inventory = process_delivery(inventory, newstock)
        calculated_tax = calculate_tax(inventory)
        print("Total stock entries entered:", inventory, "Tax amount for this entry:", calculated_tax)
        print("Please enter the next stock quantity or type 'quit' to exit.")
    elif get_valid_input(userinput) is False:
        rejectcounter += 1
        print("Invalid input. Please enter a valid number or type 'quit' to exit.")