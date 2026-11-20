from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct

# 1. Create a Supplier object (no products exist yet)
supplier = Supplier("S001", "Acme Trading Pte Ltd", "sales@acme.example")
print("1. Supplier created on its own:")
supplier.display_information()

# 2. Create a PhysicalProduct and a DigitalProduct using that Supplier
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 1.8)
ebook = DigitalProduct("D001", "Python Ebook", 15.00, 999, supplier, 4.5)
print("\n2. Products created:")
laptop.display_information()
ebook.display_information()

# 3. Display the supplier information through each Product
print("\n3. Supplier information through each product:")
print("Via laptop:")
laptop.display_supplier_information()
print("Via ebook:")
ebook.display_supplier_information()

# 4. Confirm the objects are separate and independent
print("\n4. Separate objects:")
print("   laptop is ebook:", laptop is ebook)                       # False
print("   laptop is supplier:", laptop is supplier)                 # False
print("   laptop.supplier is supplier:", laptop.supplier is supplier)   # True (a reference)
print("   laptop.supplier is ebook.supplier:", laptop.supplier is ebook.supplier)  # True (shared)

# Independence: deleting a product does not affect the Supplier
del laptop
print("\n   After del laptop, supplier still works:")
supplier.display_information()
print("   Ebook still works:")
ebook.display_supplier_information()

# Independence: deleting the supplier variable does not affect the remaining product
del supplier
print("\n   After del supplier, ebook still has its supplier:")
ebook.display_supplier_information()