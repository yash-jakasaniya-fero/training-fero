from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from .filters import OrderFilters
from .models import Customer, Product, Order, OrderItem, Invoice
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, \
    OrderCreateSerializer, ListOrderSerializer, InvoiceValidationsSerializer, InvoiceCreateSerializer
from rest_framework.filters import SearchFilter

# Customer Views
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# Product Views
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# List all OrderItems
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


#Order Views
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OrderFilters
    search_fields = ['order_number']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ListOrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ListOrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer =OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#invoice view
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceValidationsSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request, *args, **kwargs):
        invoices_data = request.data
        validation_serializer = InvoiceValidationsSerializer(data=invoices_data, many=True)

        if validation_serializer.is_valid():
            # create_serializer = InvoiceCreateSerializer(data=invoices_data, many=True)

            if create_serializer.is_valid():
                create_serializer.save()
                return Response({"data": "successfully added"}, status=status.HTTP_201_CREATED)
            else:
                return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(validation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)