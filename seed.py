from app import Flask
from models import db, Category, Product

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ahmed:ahmed123@localhost/beauty_shop"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    
    Product.query.delete()
    Category.query.delete()
    
    
    skincare = Category(name="Skincare", description="Products for skin health and beauty")
    makeup = Category(name="Makeup", description="Cosmetics and beauty products")
    haircare = Category(name="Haircare", description="Hair treatment and styling products")
    
    db.session.add_all([skincare, makeup, haircare])
    db.session.commit()
    
    
    products = [
        Product(name="Face Cream", description="Moisturizing face cream", price=25.99, stock=50, category_id=skincare.id, image_url="https://example.com/face-cream.jpg"),
        Product(name="Serum", description="Anti-aging serum", price=45.00, stock=30, category_id=skincare.id, image_url="https://example.com/serum.jpg"),
        Product(name="Lipstick", description="Long-lasting lipstick", price=15.99, stock=100, category_id=makeup.id, image_url="https://example.com/lipstick.jpg"),
        Product(name="Foundation", description="Full coverage foundation", price=35.00, stock=40, category_id=makeup.id, image_url="https://example.com/foundation.jpg"),
        Product(name="Shampoo", description="Nourishing shampoo", price=12.99, stock=80, category_id=haircare.id, image_url="https://example.com/shampoo.jpg"),
        Product(name="Conditioner", description="Deep conditioning treatment", price=14.99, stock=75, category_id=haircare.id, image_url="https://example.com/conditioner.jpg"),
    ]
    
    db.session.add_all(products)
    db.session.commit()
    
    print("✅ Database seeded successfully!")
    print(f"Created {Category.query.count()} categories")
    print(f"Created {Product.query.count()} products")
