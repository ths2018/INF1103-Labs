import gc
import weakref

from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Inventory import Inventory
from Order import Order

# Setup: products exist independently, and one is also in an Inventory
supplier = Supplier("S001", "Acme Trading Pte Ltd", "sales@acme.example")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 1.8)
ebook = DigitalProduct("D001", "Python Ebook", 15.00, 999, supplier, 4.5)
inventory = Inventory()
inventory.add_product(laptop)

# 1. Create an Order and add two products with add_order_line()
order1 = Order("O001")
order1.add_order_line(laptop, 2)
order1.add_order_line(ebook, 3)

# 2. Display each order line and the total
print("1. Order 1:")
order1.display_information()
print("   Expected total:", 2 * 1200.00 + 3 * 15.00)   # 2445.0

# 3. Same Product in a different Order: each Order creates its own OrderLine
order2 = Order("O002")
order2.add_order_line(laptop, 1)

line_in_1 = order1.order_lines[0]
line_in_2 = order2.order_lines[0]
print("\n2. Same product in two orders:")
print("   Different OrderLine objects:", line_in_1 is not line_in_2)          # True
print("   Same Product object:        ", line_in_1.product is line_in_2.product)  # True
print("   Both are the original laptop:", line_in_1.product is laptop)        # True
print("   OrderLine ids differ:", id(line_in_1) != id(line_in_2))

# 4. Remove an order line through an Order method
print("\n3. Remove the ebook line from Order 1:")
print("   Removed:", order1.remove_order_line("D001"))   # True
order1.display_information()
print("   Ebook still exists on its own:", ebook.name, "| stock", ebook.stock)

# 5. Remove the whole Order: its lines go with it, products survive
line_ref = weakref.ref(order2.order_lines[0])   # watches the line without keeping it alive
del line_in_1, line_in_2                         # drop our own references to the lines
del order2
gc.collect()
print("\n4. After del order2:")
print("   OrderLine destroyed with its Order:", line_ref() is None)   # True
print("   Laptop still exists:", laptop.name)
print("   Laptop still in Inventory:", inventory.find_product("P001") is laptop)  # True