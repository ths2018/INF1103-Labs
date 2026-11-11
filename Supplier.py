class Supplier:
    def __init__(self, supplier_id, name, contact_email):
            self.supplier_id = supplier_id
            self.name = name
            self.contact_email = contact_email

    def display_information(self):
        """Print the supplier's details."""
        print(f"Supplier ID : {self.supplier_id}")
        print(f"Name        : {self.name}")
        print(f"Contact     : {self.contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }

    @staticmethod
    def from_dict(data: dict[str, str]) -> "Supplier":
        return Supplier(data["supplier_id"], data["name"], data["contact_email"])

if __name__ == "__main__":
    supplier = Supplier("S001", "Acme Trading Pte Ltd", "sales@acme.example")
    supplier.display_information()