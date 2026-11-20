from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Inventory import Inventory

supplier = Supplier("S001", "Acme Trading Pte Ltd", "sales@acme.example")

inventory = Inventory()
inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 1.8))
inventory.add_product(DigitalProduct("D001", "Python Ebook", 15.00, 999, supplier, 4.5))

# What I predicted, keyed by product ID (not by class)
expected = {
    "P001": "This product requires physical shipping.",
    "D001": "This product is delivered digitally.",
}

# ONE loop over the Product collection: no isinstance(), no separate loops
for product in inventory.get_products():
    print("--", product.product_id)
    product.display_information()
    info = product.get_fulfilment_info()
    print(info)
    assert info == expected[product.product_id], "prediction did not match"

print("\nAll predictions matched.")