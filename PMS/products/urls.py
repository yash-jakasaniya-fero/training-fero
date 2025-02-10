from django.urls import path
from .views import product_list, product_detail, manufacturer_list, manufacturer_detail, ProductListView, \
    ProductDetailView

urlpatterns = [
    # JSON Endpoints
    path("products/", product_list, name="api_product_list"),
    path("products/<int:pk>/", product_detail, name="api_product_detail"),
    path("manufacturers/", manufacturer_list, name="api_manufacturer_list"),
    path("manufacturers/<int:pk>/", manufacturer_detail, name="api_manufacturer_detail"),

    # HTML Views
    path("temp_products/", ProductListView.as_view(), name="product_list"),
    path("temp_products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]

