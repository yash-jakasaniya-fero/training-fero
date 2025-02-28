from django.core.validators import MaxValueValidator
from django.utils.datetime_safe import date
from orders.models import Customer, Product, Order, OrderItem, Invoice
from rest_framework import serializers
from datetime import date, datetime


# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'customer_name', 'contact_number', 'email']

    def validate_customer_name(self, value):
        if Customer.objects.filter(customer_name=value).exists():
            raise serializers.ValidationError("Customer name must be unique.")
        return value

    def validate_email(self, value):
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email must be unique.")
        return value


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'weight']

    def validate_product_name(self, value):
        if Product.objects.filter(product_name=value).exists():
            raise serializers.ValidationError("Product name must be unique.")
        return value

    def validate_weight(self, value):
        if value <= 0 or value > 25:
            raise serializers.ValidationError("Product weight must be positive and not exceed 25kg.")
        return value


# OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(validators=[MaxValueValidator(25)])
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']


# Order Serializer

class OrderSerializer(serializers.ModelSerializer):
    order_item = serializers.ListField(required=True, write_only=True, child=serializers.DictField())

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer', 'order_date', 'address', 'order_item']

    def validate_order_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value


class ListOrderSerializer(serializers.ModelSerializer):
    order_item = serializers.ListField(required=True, write_only=True, child=serializers.DictField())

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer', 'order_date', 'address', 'order_item']



class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = serializers.ListField(required=True, write_only=True, child=serializers.DictField())

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer', 'order_date', 'address', 'order_items']

    def validate_order_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value

    def validate(self, data):
        order_items = data.get('order_items', [])
        total_weight = 0

        for item in order_items:
            product = item.pop('product')
            if Product.objects.filter(id=product).exists():
                item["product"] = Product.objects.get(id=product)
                total_weight = total_weight + (item.get("quantity") * item.get("product").weight)
            else:
                raise serializers.ValidationError(f"No product exist with id: {product}")

        if total_weight > 150:
            raise serializers.ValidationError("150kg")

        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

#Invoice Validations Serializers
class InvoiceValidationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_code', 'date', 'total_price', 'customer_name']

    def validate_invoice_code(self, value):
        if Invoice.objects.filter(invoice_code=value).exists():
            raise serializers.ValidationError(f"Invoice with code {value} already exists, try a unique code.")
        return value

    def validate_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("The invoice date cannot be in the past.")
        return value

    def validate_total_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total price must be a positive value.")
        return value

#Invoice Create Serializers
class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_code', 'date', 'total_price', 'customer_name']

    def create(self, validated_data):
        return Invoice.objects.create(**validated_data)