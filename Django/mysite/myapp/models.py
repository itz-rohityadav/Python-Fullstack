from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)   # Text field, max 100 characters
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Decimal field for money
    description = models.TextField()  # Large text
    stock_quantity = models.PositiveIntegerField()  # Positive whole number

    def __str__(self):
        return self.name  # For better display in admin etc.