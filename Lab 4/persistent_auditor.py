stock = 0
FILENAME = "inventory.txt"

def load_inventory(filename):
    orders = []
    with open(filename, "a") as file:
        pass

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                orders.append(line)
    return orders

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

def main():

    print("Current Orders:\n")
    current_orders = load_inventory(FILENAME)
    if current_orders:
        for order in current_orders:
            print(order)
    new_orders = []
    rejectcounter = 0
    next_id = 1001 + len(current_orders)

    while True:
        product_name = input("\nEnter Product Name:")
        if get_valid_input(product_name) is None:
            #print(generate_report(inventory, rejectcounter))
            break
        quantity = input("Enter Quantity:")
        if get_valid_input(quantity) is None:
            break
        elif get_valid_input(quantity) is True:
            newstock = int(quantity)
            new_order = f"{next_id}, {product_name}, {newstock}"
            new_orders.append(new_order)
            print("New Order Added:\n",new_order)
            next_id += 1
            #stock = process_delivery(stock, newstock)
            #calculated_tax = calculate_tax(stock)
            #print("Total stock entries entered:", stock, "Tax amount for this entry:", calculated_tax)
            #print("Please enter the next stock quantity or type 'quit' to exit.")
        elif get_valid_input(quantity) is False:
            rejectcounter += 1
            print("Invalid input. Please enter a valid number or type 'quit' to exit.")

if __name__ == "__main__":
    main()