from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    ManufacturerListView, ManufacturerDetailView, ManufacturerCreateView, ManufacturerUpdateView, ManufacturerDeleteView,
    product_list, product_detail, manufacturer_list, manufacturer_detail
)

urlpatterns = [
    # CBVs
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('manufacturers/', ManufacturerListView.as_view(), name='manufacturer_list'),
    path('manufacturers/<int:pk>/', ManufacturerDetailView.as_view(), name='manufacturer_detail'),
    path('manufacturers/create/', ManufacturerCreateView.as_view(), name='manufacturer_create'),
    path('manufacturers/<int:pk>/edit/', ManufacturerUpdateView.as_view(), name='manufacturer_update'),
    path('manufacturers/<int:pk>/delete/', ManufacturerDeleteView.as_view(), name='manufacturer_delete'),

    # FBVs
    path('js/products/', product_list, name='api_product_list'),
    path('js/products/<int:pk>/', product_detail, name='api_product_detail'),
    path('js/manufacturers/', manufacturer_list, name='api_manufacturer_list'),
    path('js/manufacturers/<int:pk>/', manufacturer_detail, name='api_manufacturer_detail'),
]