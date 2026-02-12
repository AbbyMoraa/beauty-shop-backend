# Beauty Shop - Admin Dashboard & Analytics Backend

## Your Part: Rainer - Admin Dashboard & Analytics

### Backend Features
- Admin-only APIs with JWT authentication
- View all orders
- Filter orders by date and category
- Product sales analytics
- Order analytics
- User management (update role, disable users)
- Export reports to CSV

---

## File Structure

```
backend/
├── admin/
│   ├── __init__.py
│   └── routes/
│       └── admin_routes.py    # All admin API endpoints
├── app.py                      # Test Flask app (for demo only)
└── requirements.txt            # Dependencies
```

---

## API Endpoints

All endpoints require JWT authentication (`@jwt_required()`)

### Orders
- `GET /api/admin/orders` - Get all orders with optional filters
  - Query params: `?date=2024-01-15&category=Skincare`

### Analytics
- `GET /api/admin/analytics/products` - Get product sales analytics
- `GET /api/admin/analytics/orders` - Get order statistics

### User Management
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/users/<id>` - Update user role
- `POST /api/admin/users/<id>/disable` - Disable user account

### Export
- `GET /api/admin/export/orders` - Export orders to CSV
- `GET /api/admin/export/orders/pdf` - Export orders to PDF

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Standalone (for testing)
```bash
python app.py
```
Server runs on `http://localhost:5000`

---

## Integration Instructions for Teammates

### Step 1: Register Blueprint
In your main `app.py`, add:

```python
from admin.routes.admin_routes import admin_bp

app.register_blueprint(admin_bp)
```

### Step 2: Replace Mock Data with Database
Open `admin/routes/admin_routes.py` and replace all `TODO` comments with actual database queries:

```python
# Example:
# TODO: Replace with actual database query
orders = Order.query.all()  # Replace mock_orders
```

### Step 3: Ensure JWT is Set Up
Make sure your auth module provides JWT tokens that the frontend can use.

---

## Mock Data (for testing)

The routes use mock data so you can test without a database:
- 3 sample orders
- 2 sample users
- 3 sample products

Replace these with actual database queries when integrating.

---

## Dependencies
- Flask - Web framework
- flask-jwt-extended - JWT authentication
- flask-cors - CORS support
- psycopg2-binary - PostgreSQL adapter
- reportlab - PDF generation

---

## Notes
- All routes are protected with `@jwt_required()`
- CSV export uses Python's built-in `csv` module
- PDF export uses `reportlab` library
- Filters are applied via query parameters
- Mock data allows testing before database is ready
