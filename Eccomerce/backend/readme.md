# E-Commerce API

A simple E-Commerce API built using Django Rest Framework to manage customers, products, and orders.

## Features

- **Customers**: Create, update, and list customers.
- **Products**: Create and list products.
- **Orders**: Create, update, and list orders. Each order can have multiple products.
- **Order Items**: Manage products in orders with quantities.
- **Filters**: Filter orders by customer and product.

## Models

- **Customer**: `id`, `name`, `contact_number`, `email`
- **Product**: `id`, `name`, `weight`
- **Order**: `id`, `order_number`, `customer`, `order_date`, `address`
- **Order Item**: `id`, `order`, `product`, `quantity`

## API Endpoints

- **Customers**:
  - `GET /api/customers/` - List all customers
  - `POST /api/customers/` - Create a new customer
  - `PUT /api/customers/<id>/` - Update a customer
  
- **Products**:
  - `GET /api/products/` - List all products
  - `POST /api/products/` - Create a new product
  
- **Orders**:
  - `GET /api/orders/` - List all orders
  - `POST /api/orders/` - Create a new order
  - `PUT /api/orders/<id>/` - Edit an order
  - `GET /api/orders/?products=Book,Pen` - Filter by product
  - `GET /api/orders/?customer=Sam` - Filter by customer

## Validations

- Unique customer and product names.
- Product weight should be positive and ≤ 25kg.
- Order weight must be ≤ 150kg.
- Order date cannot be in the past.
