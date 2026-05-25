import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# Create tables and seed data if empty
try:
    with app.app_context():
        from models import db, Category, Product
        db.create_all()
        if Category.query.count() == 0:
            from seed import seed_products
            seed_products()
except Exception as e:
    print(f"Warning: Could not create tables or seed data: {e}")

if __name__ == "__main__":
    app.run()
