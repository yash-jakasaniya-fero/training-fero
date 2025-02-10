from django.http import JsonResponse
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from .models import Product, Manufacturer

# JSON Views
def product_list(request):
    products = Product.objects.all().values("id", "name", "manufacturer__name", "price", "quantity")
    return JsonResponse(list(products), safe=False)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = {
        "name": product.name,
        "manufacturer": product.manufacturer.name,
        "description": product.description,
        "price": product.price,
        "shipping_cost": product.shipping_cost,
        "quantity": product.quantity,
    }
    return JsonResponse(data)

def manufacturer_list(request):
    manufacturers = Manufacturer.objects.filter(active=True).values("id", "name", "location")
    return JsonResponse(list(manufacturers), safe=False)

def manufacturer_detail(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    products = manufacturer.products.values("id", "name", "price")
    data = {
        "name": manufacturer.name,
        "location": manufacturer.location,
        "products": list(products),
    }
    return JsonResponse(data)

# HTML Views
class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"