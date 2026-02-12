# Beauty Shop API Documentation

Base URL: `http://localhost:5000`

## Authentication

### Register
**POST** `/register`

```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

Response: `201 Created`
```json
{
  "message": "registered successfully"
}
```

### Login
**POST** `/login`

```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

Response: `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Products

### Get All Products
**GET** `/products`

Response: `200 OK`
```json
[
  {
    "id": 1,
    "name": "Face Cream",
    "description": "Moisturizing cream",
    "price": 25.99,
    "image_url": "https://...",
    "stock": 50,
    "category_id": 1,
    "category_name": "Skincare"
  }
]
```

### Get Categories
**GET** `/categories`

Response: `200 OK`
```json
[
  {
    "id": 1,
    "name": "Skincare",
    "description": "Skincare products"
  }
]
```

## Cart
*Requires JWT token in Authorization header: `Bearer <token>`*

### View Cart
**GET** `/cart`

Response: `200 OK`
```json
[
  {
    "product_id": 1,
    "quantity": 2,
    "product_name": "Face Cream",
    "price": 25.99
  }
]
```

### Add to Cart
**POST** `/cart`

```json
{
  "product_id": 1,
  "quantity": 2
}
```

Response: `201 Created`
```json
{
  "message": "added to cart"
}
```

## Checkout
*Requires JWT token*

### Checkout
**POST** `/checkout`

Response: `201 Created`
```json
{
  "message": "checkout complete",
  "order_id": 5,
  "total": 51.98
}
```

## Payments
*Requires JWT token*

### Simulate Payment (Testing)
**POST** `/payments/simulate`

```json
{
  "order_id": 5
}
```

Response: `200 OK`
```json
{
  "message": "payment successful",
  "order_id": 5,
  "payment_status": "PAID",
  "invoice_number": "INV-A3F2B1C4"
}
```

### Initiate Real Payment (M-Pesa)
**POST** `/payments/initiate`

```json
{
  "order_id": 5,
  "phone_number": "254712345678"
}
```

Response: `200 OK` or `503 Service Unavailable`

### Payment Callback (Webhook)
**POST** `/payments/callback`

Internal endpoint for Payd API callbacks.

## Invoices
*Requires JWT token*

### Get Invoice
**GET** `/invoices/<order_id>`

Response: `200 OK`
```json
{
  "invoice_number": "INV-A3F2B1C4",
  "order_id": 5,
  "amount": 51.98,
  "status": "PAID",
  "created_at": "2024-01-15T10:30:00",
  "order_details": {
    "transaction_ref": "TXN123",
    "payment_status": "PAID",
    "items": [
      {
        "product_id": 1,
        "quantity": 2,
        "unit_price": 25.99
      }
    ]
  }
}
```

## Addresses
*Requires JWT token*

### Create Address
**POST** `/addresses`

```json
{
  "full_name": "John Doe",
  "phone_number": "254712345678",
  "address_line": "123 Main St",
  "city": "Nairobi",
  "postal_code": "00100",
  "address_type": "billing"
}
```

Response: `201 Created`
```json
{
  "message": "address saved",
  "id": 1
}
```

### Get Addresses
**GET** `/addresses`

Response: `200 OK`
```json
[
  {
    "id": 1,
    "full_name": "John Doe",
    "phone_number": "254712345678",
    "address_line": "123 Main St",
    "city": "Nairobi",
    "postal_code": "00100",
    "address_type": "billing"
  }
]
```

## Error Responses

All endpoints return errors in this format:

```json
{
  "error": "error message here"
}
```

Common status codes:
- `400` - Bad request (missing fields)
- `401` - Unauthorized (invalid credentials or missing token)
- `404` - Not found
- `503` - Service unavailable (payment service down)

## Notes

- All authenticated endpoints require `Authorization: Bearer <token>` header
- Use `/payments/simulate` for testing without real M-Pesa charges
- Use `/payments/initiate` for production M-Pesa payments (requires Payd account setup)
