from django.urls import path
from orders.views import CustomerViewSet, ProductViewSet, OrderViewSet , OrderItemViewSet
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


from django.urls import path


urlpatterns = [
    # Customer URLs
    path('customers/', CustomerViewSet.as_view({'get': 'list', 'post': 'create'}), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),name='customer-detail'),

    #Product  URLs
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list-create'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),name='product-detail'),

    # Order URLs
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list-create'),
    path('orders/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='order-detail'),

    # Order-Item URLs
    path('order-items/', OrderItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='order_item-list-create'),
    path('order-items/<int:pk>/', OrderItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='order_item-details')

]





