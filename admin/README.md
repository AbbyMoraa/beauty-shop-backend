# Admin Module

This is the admin part of the beauty shop backend. It has all the admin stuff like viewing orders, analytics, and managing users.

## How to test it

1. Install stuff:
```bash
pip install -r requirements.txt
```

2. Run the test server:
```bash
cd admin
python app.py
```

3. Go to http://localhost:5000 and you'll see the endpoints

4. First go to /login to get a token, then use that token for other endpoints

## Endpoints

- `/api/admin/orders` - see all orders (can filter by date and category)
- `/api/admin/analytics/products` - product sales data
- `/api/admin/analytics/orders` - order statistics  
- `/api/admin/users` - list all users
- `/api/admin/users/<id>` - update user role (PUT)
- `/api/admin/users/<id>/disable` - disable a user (POST)
- `/api/admin/export/orders` - download orders as CSV
- `/api/admin/export/orders/pdf` - download orders as PDF

## Notes

- All endpoints need JWT authentication
- Using mock data for now (check the TODO comments in admin_routes.py)
- When integrating with main app, replace mock data with real database queries
- The test app gives you a token without checking credentials (just for testing)

## Integration

To use this in the main app, just register the blueprint:

```python
from admin.routes.admin_routes import admin_bp
app.register_blueprint(admin_bp)
```

Then replace all the mock data with real database queries.