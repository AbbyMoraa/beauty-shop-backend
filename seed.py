from app import app, db
from models import Product, CartItem

def seed_data():
    with app.app_context():
        # Clear existing data (optional, for clean runs)
        db.session.query(CartItem).delete()
        db.session.query(Product).delete()

        # Add sample products
        products = [
            Product(name="Shampoo", price=5.99),
            Product(name="Conditioner", price=6.49),
            Product(name="Hair Dryer", price=29.99),
        ]
        db.session.add_all(products)
        db.session.commit()

        # Add sample cart items for user_id=1
        cart_items = [
            CartItem(user_id=1, product_id=products[0].id, quantity=2),
            CartItem(user_id=1, product_id=products[2].id, quantity=1),
        ]
        db.session.add_all(cart_items)
        db.session.commit()

        print("✅ Seed data inserted successfully!")

if __name__ == "__main__":
    seed_data()