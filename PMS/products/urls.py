from django.urls import path
from .views import product_list, product_detail, manufacturer_list, manufacturer_detail, ProductListView, \
    ProductDetailView

urlpatterns = [
    # JSON Endpoints
    path("api/products/", product_list, name="api_product_list"),
    path("api/products/<int:pk>/", product_detail, name="api_product_detail"),
    path("api/manufacturers/", manufacturer_list, name="api_manufacturer_list"),
    path("api/manufacturers/<int:pk>/", manufacturer_detail, name="api_manufacturer_detail"),

    # HTML Views
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
