import django_filters
from django_filters import rest_framework

from orders.models import Order, OrderItem


class OrderFilters(rest_framework.FilterSet):
    customer = django_filters.CharFilter(method='filter_by_customer_name')
    products = django_filters.CharFilter(method='filter_by_product_names')
    class Meta:
        model = Order
        fields = ['customer', 'products']

    def filter_by_customer_name(self, queryset, key, value ):
        return queryset.filter(customer__customer_name__icontains=value)

    def filter_by_product_names(self, queryset, name, value):
        value = value.split(",")
        order_items_ids = list(OrderItem.objects.filter(product__product_name__in=value).values_list('order__id', flat=True))
        return queryset.filter(id__in=order_items_ids)

