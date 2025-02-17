from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Manufacturer
from .forms import ProductForm, ManufacturerForm

# CBV - Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

# CBV - Manufacturer Views
class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'manufacturer_list.html'

class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'manufacturer_detail.html'

class ManufacturerCreateView(CreateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'manufacturer_form.html'
    success_url = reverse_lazy('manufacturer_list')

class ManufacturerUpdateView(UpdateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'manufacturer_form.html'
    success_url = reverse_lazy('manufacturer_list')

class ManufacturerDeleteView(DeleteView):
    model = Manufacturer
    template_name = 'manufacturer_confirm_delete.html'
    success_url = reverse_lazy('manufacturer_list')

# FBVs - JSON Responses
def product_list(request):
    products = list(Product.objects.values())
    return JsonResponse({'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return JsonResponse({'id': product.id, 'name': product.name, 'price': product.price})

def manufacturer_list(request):
    manufacturers = list(Manufacturer.objects.values())
    return JsonResponse({'manufacturers': manufacturers})

def manufacturer_detail(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    return JsonResponse({'id': manufacturer.id, 'name': manufacturer.name, 'location': manufacturer.location})