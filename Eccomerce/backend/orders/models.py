from django.db import models


class Customer(models.Model):
    customer_name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=15, default="N/A")
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.customer_name


class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.all().order_by('id').last()
            if last_order:
                new_order_number = f"ORD{str(last_order.id + 1).zfill(5)}"
            else:
                new_order_number = "ORD00001"
            self.order_number = new_order_number
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order.order_number} - {self.product.product_name}"

