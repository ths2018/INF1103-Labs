from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from Inventory import Inventory

# 1. Create the Product BEFORE any Inventory exists
supplier = Supplier("S001", "Acme Trading Pte Ltd", "sales@acme.example")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 1.8)
print("1. Product created with no inventory:")
laptop.display_information()

# 2. Add it to Inventory A
inventory_a = Inventory()
inventory_a.add_product(laptop)
print("\n2. Added to Inventory A:")
print("   Same object, not a copy:", inventory_a.find_product("P001") is laptop)

# 3. Remove it from Inventory A, then confirm the Product still works
inventory_a.remove_product("P001")
print("\n3. Removed from Inventory A:")
print("   Still in A?", inventory_a.find_product("P001"))   # None
laptop.display_information()
laptop.display_supplier_information()
laptop.update_stock(20)
print("   Stock updated after removal:", laptop.stock)      # 20

# 4. Add the SAME object to Inventory B
inventory_b = Inventory()
inventory_b.add_product(laptop)
print("\n4. Added to Inventory B:")
print("   Same object as before:", inventory_b.find_product("P001") is laptop)

# 5. Removing from an inventory does not destroy the Product
inventory_b.remove_product("P001")
print("\n5. Removed from Inventory B:")
print("   Still in B?", inventory_b.find_product("P001"))   # None
print("   Product still usable:", laptop.name, "| stock", laptop.stock)