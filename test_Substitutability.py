from Supplier import Supplier
from Product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Inventory import Inventory


def show_product_details(product: Product) -> None:
    """Uses only behaviour that every Product supports."""
    product.display_information()
    print(product.get_fulfilment_info())


def check_stock_contract(product: Product) -> None:
    """The expectation Product sets for update_stock(), checked on any Product."""
    product.update_stock(5)
    assert product.stock == 5, "valid update should set the stock"

    try:
        product.update_stock(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid stock should raise ValueError")
    assert product.stock == 5, "a rejected update should leave stock unchanged"
    print(f"   {product.name}: stock contract holds")


supplier = Supplier("S001", "Acme Trading Pte Ltd", "sales@acme.example")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 1.8)
ebook = DigitalProduct("D001", "Python Ebook", 15.00, 999, supplier, 4.5)

# 1. Same function, both subclasses, no changes
print("1. show_product_details with each subclass:")
products: list[Product] = [laptop, ebook]
for p in products:
    show_product_details(p)

# 2. Both types in one Inventory, used through normal operations
print("\n2. Inventory operations:")
inventory = Inventory()
print("   Added:", inventory.add_product(laptop), inventory.add_product(ebook))  # True True
inventory.display_all()
print("   Find P001:", inventory.find_product("P001") is laptop)                # True
print("   Find D001:", inventory.find_product("D001") is ebook)                 # True
print("   Search '001' finds both:", len(inventory.search_product("001")) == 2) # True

# 3. Same stock expectations hold for both
print("\n3. update_stock contract:")
for p in inventory.get_products():
    check_stock_contract(p)

# 4. Same persistence behaviour
print("\n4. to_dict:")
for p in inventory.get_products():
    d = p.to_dict()
    print("  ", d["product_id"], d["stock"], d["supplier_id"])

# 5. Removal works the same way
print("\n5. remove_product:", inventory.remove_product("P001"), inventory.remove_product("D001"))