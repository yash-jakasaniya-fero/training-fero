from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views import CustomerViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, InvoiceViewSet

router = DefaultRouter()

router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'invoices', InvoiceViewSet, basename='Invoice')

urlpatterns = [
    path('', include(router.urls)),
]
