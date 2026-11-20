"""Lab 9, Section 7: automated tests for the Strategy pattern, Factory pattern,
validation and exception handling.

Run from the project folder (the one that holds Order.py, Product.py, ...):

    python -m unittest discover -s tests -v

(pytest also works:  python -m pytest tests -v)

Assumed file layout, all in the project folder:
    Supplier, Product, PhysicalProduct, DigitalProduct, Inventory, Order, OrderLine,
    DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount,
    ProductFactory           (one class per file, file name = class name)
    Input_helpers.py         holds get_positive_float
    File_handling.py         holds load_products
If you put something elsewhere, change the imports below.
"""
import ast
import contextlib
import inspect
import io
import os
import re
import sys
import tempfile
import textwrap
import unittest
from unittest.mock import patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from Supplier import Supplier
from Product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Inventory import Inventory
from Order import Order
from OrderLine import OrderLine
from DiscountStrategy import DiscountStrategy
from NoDiscount import NoDiscount
from PercentageDiscount import PercentageDiscount
from BulkDiscount import BulkDiscount
from StudentDiscount import StudentDiscount
from ProductFactory import ProductFactory
from Input_Helper import get_positive_float
from File_handling import load_products

LAB_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


# ---------------- helpers ----------------
def run_quietly(func, *args):
    """Call func while capturing what it prints. Returns (result, printed_text)."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


def make_supplier() -> Supplier:
    return Supplier("S001", "Acme Trading Pte Ltd", "sales@acme.example")


def order_worth_250(discount: DiscountStrategy | None = None) -> Order:
    """An order whose lines add up to exactly 250."""
    keyboard = ProductFactory.create("physical", "P010", "Keyboard", 50.00, 10, make_supplier(), 0.9)
    order = Order("O001", discount)
    order.add_order_line(keyboard, 5)
    return order


def read_project_file(filename: str) -> str:
    path = os.path.join(ROOT, filename)
    with open(path, encoding="utf-8") as file:
        return file.read()


def broad_except_lines(filename: str) -> list[int]:
    """Line numbers of any bare 'except:' or 'except Exception/BaseException' in a file."""
    tree = ast.parse(read_project_file(filename))
    broad = {"Exception", "BaseException"}
    lines = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        caught = node.type
        if caught is None:
            lines.append(node.lineno)
        elif isinstance(caught, ast.Name) and caught.id in broad:
            lines.append(node.lineno)
        elif isinstance(caught, ast.Tuple) and any(
                isinstance(item, ast.Name) and item.id in broad for item in caught.elts):
            lines.append(node.lineno)
    return lines


# =====================================================================
class TestStrategyPattern(unittest.TestCase):
    """Order calculates totals through a DiscountStrategy."""

    def test_order_with_no_strategy_given_has_no_discount(self):
        self.assertAlmostEqual(order_worth_250().calculate_total(), 250.0)

    def test_total_is_passed_through_the_strategy(self):
        with self.subTest("NoDiscount"):
            self.assertAlmostEqual(order_worth_250(NoDiscount()).calculate_total(), 250.0)
        with self.subTest("BulkDiscount(200, 20) on 250"):
            self.assertAlmostEqual(order_worth_250(BulkDiscount(200, 20)).calculate_total(), 230.0)
        with self.subTest("PercentageDiscount(10) on 250"):
            self.assertAlmostEqual(order_worth_250(PercentageDiscount(10)).calculate_total(), 225.0)
        with self.subTest("StudentDiscount on 250"):
            self.assertAlmostEqual(order_worth_250(StudentDiscount()).calculate_total(), 237.5)

    def test_bulk_discount_threshold(self):
        keyboard = ProductFactory.create("physical", "P011", "Keyboard", 50.00, 10, make_supplier(), 0.9)
        below = Order("O002", BulkDiscount(200, 20))
        below.add_order_line(keyboard, 3)                      # 150: under the threshold
        self.assertAlmostEqual(below.calculate_total(), 150.0)
        exact = Order("O003", BulkDiscount(200, 20))
        exact.add_order_line(keyboard, 4)                      # 200: exactly on the threshold
        self.assertAlmostEqual(exact.calculate_total(), 180.0)

    def test_empty_order_total_is_zero(self):
        self.assertAlmostEqual(Order("O004", PercentageDiscount(10)).calculate_total(), 0.0)

    def test_all_strategies_are_discount_strategies(self):
        for strategy in (NoDiscount(), PercentageDiscount(10), BulkDiscount(200, 20), StudentDiscount()):
            with self.subTest(type(strategy).__name__):
                self.assertIsInstance(strategy, DiscountStrategy)

    def test_discount_strategy_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_order_contains_no_discount_branching(self):
        """calculate_total must not choose between discounts with if/elif."""
        source = textwrap.dedent(inspect.getsource(Order.calculate_total))
        branches = [node for node in ast.walk(ast.parse(source))
                    if isinstance(node, (ast.If, ast.IfExp))]
        self.assertEqual(branches, [], "calculate_total should only add up lines and call apply()")

    def test_order_does_not_know_the_concrete_strategies(self):
        source = inspect.getsource(Order).lower()
        for word in ("percentage", "bulk", "student"):
            with self.subTest(word):
                self.assertNotIn(word, source, f"Order should not mention '{word}'")


class TestOpenClosed(unittest.TestCase):
    """A new strategy can be added, and swapped in, without changing Order."""

    def test_new_strategy_works_without_touching_order(self):
        class HalfPrice(DiscountStrategy):          # a brand-new strategy, defined right here
            def apply(self, total: float) -> float:
                return total / 2

        self.assertAlmostEqual(order_worth_250(HalfPrice()).calculate_total(), 125.0)

    def test_set_discount_changes_an_existing_order(self):
        order = order_worth_250(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)    # recalculated from 250, not 230
        order.set_discount(NoDiscount())
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_new_lines_use_the_current_strategy(self):
        order = order_worth_250(PercentageDiscount(10))
        extra = ProductFactory.create("digital", "D010", "Ebook", 50.00, 99, make_supplier(), 4.5)
        order.add_order_line(extra, 2)                            # 250 + 100 = 350
        self.assertAlmostEqual(order.calculate_total(), 315.0)

    def test_one_strategy_object_can_be_shared(self):
        shared = PercentageDiscount(10)
        first, second = order_worth_250(shared), order_worth_250(shared)
        self.assertAlmostEqual(first.calculate_total(), 225.0)
        self.assertAlmostEqual(second.calculate_total(), 225.0)


# =====================================================================
class TestFactory(unittest.TestCase):
    """Products are created through ProductFactory."""

    def test_factory_returns_the_right_subclass(self):
        supplier = make_supplier()
        physical = ProductFactory.create("physical", "P001", "Laptop", 1200.00, 10, supplier, 1.8)
        digital = ProductFactory.create("digital", "D001", "Ebook", 15.00, 99, supplier, 4.5)
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertIsInstance(physical, Product)
        self.assertIsInstance(digital, Product)

    def test_factory_passes_the_values_and_supplier_through(self):
        supplier = make_supplier()
        product = ProductFactory.create("physical", "P001", "Laptop", 1200.00, 10, supplier, 1.8)
        self.assertEqual(product.product_id, "P001")
        self.assertEqual(product.name, "Laptop")
        self.assertAlmostEqual(product.price, 1200.00)
        self.assertEqual(product.stock, 10)
        self.assertIs(product.supplier, supplier)

    def test_unknown_type_raises_value_error_with_a_clear_message(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, make_supplier())
        message = str(context.exception)
        self.assertIn("Unknown product type", message)
        self.assertIn("service", message)

    def test_program_code_does_not_create_products_directly(self):
        """The menu, loader and main program must go through the factory."""
        direct = re.compile(r"(?<!class )\b(PhysicalProduct|DigitalProduct)\(")
        for filename in ("InventoryMenu.py", "File_handling.py", "main.py"):
            if not os.path.exists(os.path.join(ROOT, filename)):
                continue
            with self.subTest(filename):
                offenders = [line.strip() for line in read_project_file(filename).splitlines()
                             if direct.search(line)]
                self.assertEqual(offenders, [], f"{filename} creates a product directly")


# =====================================================================
class TestValidation(unittest.TestCase):
    """Invalid prices, stock quantities and order quantities are rejected."""

    def setUp(self):
        self.supplier = make_supplier()

    def test_price_must_be_greater_than_zero(self):
        for product_type in ("physical", "digital"):
            for bad_price in (0, -5, -0.01):
                with self.subTest(product_type=product_type, price=bad_price):
                    with self.assertRaises(ValueError):
                        ProductFactory.create(product_type, "X1", "Item", bad_price, 5, self.supplier, 1.0)

    def test_a_small_positive_price_is_accepted(self):
        product = ProductFactory.create("physical", "X1", "Item", 0.01, 5, self.supplier, 1.0)
        self.assertAlmostEqual(product.price, 0.01)

    def test_stock_cannot_be_negative_at_creation(self):
        for product_type in ("physical", "digital"):
            with self.subTest(product_type):
                with self.assertRaises(ValueError):
                    ProductFactory.create(product_type, "X1", "Item", 10.0, -1, self.supplier, 1.0)

    def test_zero_stock_is_allowed(self):
        product = ProductFactory.create("digital", "X1", "Item", 10.0, 0, self.supplier, 1.0)
        self.assertEqual(product.stock, 0)

    def test_update_stock_rejects_bad_values_and_keeps_the_old_stock(self):
        for product_type in ("physical", "digital"):
            product = ProductFactory.create(product_type, "X1", "Item", 10.0, 10, self.supplier, 1.0)
            for bad_value in (-1, 2.5):
                with self.subTest(product_type=product_type, value=bad_value):
                    with self.assertRaises(ValueError):
                        product.update_stock(bad_value)
                    self.assertEqual(product.stock, 10, "a rejected update must not change stock")

    def test_order_line_quantity_must_be_greater_than_zero(self):
        product = ProductFactory.create("physical", "X1", "Item", 10.0, 10, self.supplier, 1.0)
        for bad_quantity in (0, -1, -100):
            with self.subTest(quantity=bad_quantity):
                with self.assertRaises(ValueError):
                    OrderLine(product, bad_quantity)

    def test_order_rejects_a_bad_quantity_and_stays_empty(self):
        product = ProductFactory.create("physical", "X1", "Item", 10.0, 10, self.supplier, 1.0)
        order = Order("O001")
        with self.assertRaises(ValueError):
            order.add_order_line(product, 0)
        self.assertEqual(order.order_lines, [])


# =====================================================================
class TestUserInput(unittest.TestCase):
    """Invalid input is handled without crashing, and the user is asked again."""

    def test_asks_again_until_the_price_is_valid(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as fake_input:
            result, printed = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(result, 12.5)
        self.assertIsInstance(result, float)
        self.assertEqual(fake_input.call_count, 3)
        lines = [line.lower() for line in printed.strip().splitlines()]
        self.assertEqual(len(lines), 2)
        self.assertIn("valid number", lines[0])           # reply to 'abc'
        self.assertIn("greater than zero", lines[1])      # reply to '-5'

    def test_zero_and_empty_input_are_rejected(self):
        with patch("builtins.input", side_effect=["", "0", "   ", "7"]) as fake_input:
            result, _ = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(result, 7.0)
        self.assertEqual(fake_input.call_count, 4)

    def test_a_valid_first_entry_is_returned_straight_away(self):
        with patch("builtins.input", side_effect=["19.99"]) as fake_input:
            result, printed = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(result, 19.99)
        self.assertEqual(fake_input.call_count, 1)
        self.assertEqual(printed, "")


# =====================================================================
class TestLoadProducts(unittest.TestCase):
    """A missing file and bad rows are handled gracefully."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.supplier = make_supplier()
        self.inventory = Inventory()

    def write_csv(self, text: str) -> str:
        path = os.path.join(self.folder.name, "products.csv")
        with open(path, "w", newline="", encoding="utf-8") as file:
            file.write(text)
        return path

    def ids(self) -> list[str]:
        return [product.product_id for product in self.inventory.get_products()]

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        path = self.write_csv(LAB_CSV)
        result, printed = run_quietly(load_products, path, self.inventory, self.supplier)
        self.assertIsNone(result)
        self.assertEqual(self.ids(), ["P001", "D001", "P003"])
        self.assertIn("3 products loaded", printed)
        self.assertIn("service", printed)                  # the unknown-type row was reported
        self.assertIn("abc", printed)                      # the non-numeric price row was reported
        self.assertTrue(printed.strip().endswith("Load attempt finished."))

    def test_loaded_products_have_the_right_types_and_supplier(self):
        run_quietly(load_products, self.write_csv(LAB_CSV), self.inventory, self.supplier)
        self.assertIsInstance(self.inventory.find_product("P001"), PhysicalProduct)
        self.assertIsInstance(self.inventory.find_product("D001"), DigitalProduct)
        self.assertIs(self.inventory.find_product("P003").supplier, self.supplier)
        self.assertEqual(self.inventory.find_product("P001").stock, 10)

    def test_missing_file_does_not_crash(self):
        missing = os.path.join(self.folder.name, "no_such_file.csv")
        result, printed = run_quietly(load_products, missing, self.inventory, self.supplier)
        self.assertIsNone(result)
        self.assertEqual(self.ids(), [])
        self.assertIn("not found", printed.lower())
        self.assertNotIn("products loaded", printed)       # the else block must not run
        self.assertTrue(printed.strip().endswith("Load attempt finished."))   # finally still runs

    def test_finally_message_prints_in_both_cases(self):
        _, with_file = run_quietly(load_products, self.write_csv(LAB_CSV), self.inventory, self.supplier)
        _, without_file = run_quietly(load_products, os.path.join(self.folder.name, "x.csv"),
                                      Inventory(), self.supplier)
        self.assertEqual(with_file.count("Load attempt finished."), 1)
        self.assertEqual(without_file.count("Load attempt finished."), 1)

    def test_short_and_blank_rows_do_not_stop_loading(self):
        text = ("product_type,product_id,name,price,stock_quantity\n"
                "physical,P001,Lamp,25.00,10\n"
                "\n"
                "physical,P002\n"
                "digital,D001,Editor,49.90,100\n")
        run_quietly(load_products, self.write_csv(text), self.inventory, self.supplier)
        self.assertEqual(self.ids(), ["P001", "D001"])

    def test_invalid_values_in_a_row_are_rejected_by_the_product_rules(self):
        text = ("product_type,product_id,name,price,stock_quantity\n"
                "physical,P001,Free Lamp,0,10\n"
                "physical,P002,Chair,25.00,-3\n"
                "physical,P003,Desk,25.00,2.5\n"
                "physical,P004,Stand,39.50,7\n")
        run_quietly(load_products, self.write_csv(text), self.inventory, self.supplier)
        self.assertEqual(self.ids(), ["P004"])

    def test_duplicate_ids_are_not_added_twice(self):
        text = ("product_type,product_id,name,price,stock_quantity\n"
                "physical,P001,Lamp,25.00,10\n"
                "physical,P001,Lamp again,30.00,5\n")
        run_quietly(load_products, self.write_csv(text), self.inventory, self.supplier)
        self.assertEqual(self.ids(), ["P001"])
        self.assertEqual(self.inventory.find_product("P001").name, "Lamp")

    def test_file_with_only_a_header_loads_nothing(self):
        path = self.write_csv("product_type,product_id,name,price,stock_quantity\n")
        _, printed = run_quietly(load_products, path, self.inventory, self.supplier)
        self.assertEqual(self.ids(), [])
        self.assertIn("0 products loaded", printed)


# =====================================================================
class TestExceptionStyle(unittest.TestCase):
    """Each except catches a specific exception."""

    def test_no_bare_or_overly_broad_except_in_the_error_handling_code(self):
        for filename in ("Input_Helper.py", "File_handling.py"):
            with self.subTest(filename):
                self.assertTrue(os.path.exists(os.path.join(ROOT, filename)),
                                f"expected {filename} in the project folder")
                self.assertEqual(broad_except_lines(filename), [],
                                 f"{filename} has a bare 'except:' or 'except Exception' "
                                 "(line numbers shown above)")

    def test_load_products_uses_try_except_else_finally(self):
        tree = ast.parse(textwrap.dedent(inspect.getsource(load_products)))
        tries = [node for node in ast.walk(tree) if isinstance(node, ast.Try)]
        self.assertTrue(any(t.handlers and t.orelse and t.finalbody for t in tries),
                        "load_products should use try / except / else / finally")
        caught = {handler.type.id for t in tries for handler in t.handlers
                  if isinstance(handler.type, ast.Name)}
        self.assertIn("FileNotFoundError", caught)
        self.assertIn("ValueError", caught)


if __name__ == "__main__":
    unittest.main(verbosity=2)
