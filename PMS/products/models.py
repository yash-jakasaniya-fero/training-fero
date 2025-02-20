from django.db import models

# Manufacturer Model
class Manufacturer(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SE)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='product_photos/', blank=True, null=True)
    price = models.FloatField()
    shipping_cost = models.FloatField()
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name