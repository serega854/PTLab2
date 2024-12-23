from django.test import TestCase
from shop.models import Product, ShopPurchase
from datetime import datetime
from decimal import Decimal

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="book", price=740, quantity=2,quantity_beg=2)
        Product.objects.create(name="pencil", price=50,quantity=2,quantity_beg=2)

    def test_correctness_types(self):                   
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, Decimal)
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(name="pencil").price, Decimal)        

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="book").price == 740)
        self.assertTrue(Product.objects.get(name="pencil").price == 50)


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_book = Product.objects.create(name="book", price=740,quantity="2",quantity_beg="2")
        self.datetime = datetime.now()
        ShopPurchase.objects.create(product=self.product_book,
                                person="Ivanov",
                                address="Svetlaya St.")

    def test_correctness_types(self):
        self.assertIsInstance(ShopPurchase.objects.get(product=self.product_book).person, str)
        self.assertIsInstance(ShopPurchase.objects.get(product=self.product_book).address, str)
    

    def test_correctness_data(self):
        self.assertTrue(ShopPurchase.objects.get(product=self.product_book).person == "Ivanov")
        self.assertTrue(ShopPurchase.objects.get(product=self.product_book).address == "Svetlaya St.")
        self.datetime.replace(microsecond=0)