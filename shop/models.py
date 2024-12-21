# shop/models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    quantity_beg = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class ShopPurchase(models.Model):
    person = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Purchase by {self.person} of {self.product}"
