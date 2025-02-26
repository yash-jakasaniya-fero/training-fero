from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.DecimalField

    def __str__(self):
        return self.name

class Order(models.Model):
    order_number = models.CharField(max_length=255, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField
    address = models.CharField

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first
            last_id = last_order.id if last_order else 0
            self.order_number = f'ORD{str(last_id + 1).zfill(5)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField

    def __str__(self):
        return f'{self.order.order_number} - {self.product.name} ({self.quantity})'
