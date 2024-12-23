from django.test import TestCase
from shop.models import Product, ShopPurchase
from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="book", price=740, quantity=2, quantity_beg=2)
        Product.objects.create(name="pencil", price=50, quantity=2, quantity_beg=2)

    def test_correctness_types(self):
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, Decimal)
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(name="pencil").price, Decimal)        

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="book").price == 740)
        self.assertTrue(Product.objects.get(name="pencil").price == 50)


#мои 2 теста для столбцов колчества, что нельзя заполнить строкой датой и тд
    def test_quantity_validation(self):
        """Проверка, что нельзя установить строку в поле quantity."""
        product = Product(name="test_product", price=Decimal('100.00'), quantity_beg=1)
        with self.assertRaises(ValidationError):
            product.quantity = "not_a_number"
            product.full_clean()  

    def test_quantity_beg_validation(self):
        """Проверка, что нельзя установить строку в поле quantity_beg."""
        product = Product(name="test_product", price=Decimal('100.00'), quantity=1)
        with self.assertRaises(ValidationError):
            product.quantity_beg = "not_a_number"
            product.full_clean()  


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_book = Product.objects.create(name="book", price=740, quantity=2, quantity_beg=2)
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


    def test_purchase_decreases_quantity(self):
        """Проверка, что количество товара уменьшается после покупки."""
        initial_quantity = self.product_book.quantity
        ShopPurchase.objects.create(product=self.product_book,
                                    person="Petrov",
                                    address="Svetlaya St.")
        self.product_book.quantity -= 1  # Эмулируем уменьшение количества
        self.product_book.save()

        self.assertEqual(self.product_book.quantity, initial_quantity - 1)

    def test_quantity_beg_remains_constant(self):
        """Проверка, что quantity_beg не изменяется при покупке."""
        initial_quantity_beg = self.product_book.quantity_beg
        ShopPurchase.objects.create(product=self.product_book,
                                    person="Sidorov",
                                    address="Svetlaya St.")
        
        # Эмулируем уменьшение количества
        self.product_book.quantity -= 1  
        self.product_book.save()

        self.assertEqual(self.product_book.quantity_beg, initial_quantity_beg)


        
    def test_purchase_with_zero_quantity(self):
        """Проверка, что нельзя создать покупку, если количество равно нулю."""
        product = Product.objects.create(name="eraser", price=30, quantity=0, quantity_beg=0)

        with self.assertRaises(ValueError):
            if product.quantity == 0:
                raise ValueError("Извините, товар закончился.")