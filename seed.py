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
        # Skincare - 8 products
        Product(name="Face Cream", description="Moisturizing face cream", price=2599.00, stock=50, category_id=skincare.id, image_url="https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400"),
        Product(name="Serum", description="Anti-aging serum", price=4500.00, stock=30, category_id=skincare.id, image_url="https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400"),
        Product(name="Cleanser", description="Gentle facial cleanser", price=1800.00, stock=60, category_id=skincare.id, image_url="https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400"),
        Product(name="Toner", description="Balancing toner", price=2200.00, stock=45, category_id=skincare.id, image_url="https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400"),
        Product(name="Eye Cream", description="Anti-wrinkle eye cream", price=3200.00, stock=35, category_id=skincare.id, image_url="https://images.unsplash.com/photo-1556229010-aa9e5d93b28b?w=400"),
        Product(name="Sunscreen", description="SPF 50 sunscreen", price=2800.00, stock=70, category_id=skincare.id, image_url="https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400"),
        Product(name="Face Mask", description="Hydrating face mask", price=1500.00, stock=55, category_id=skincare.id, image_url="https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400"),
        Product(name="Night Cream", description="Nourishing night cream", price=3800.00, stock=40, category_id=skincare.id, image_url="https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400"),
        
        # Makeup - 8 products
        Product(name="Lipstick", description="Long-lasting lipstick", price=1599.00, stock=100, category_id=makeup.id, image_url="https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400"),
        Product(name="Foundation", description="Full coverage foundation", price=3500.00, stock=40, category_id=makeup.id, image_url="https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400"),
        Product(name="Mascara", description="Volumizing mascara", price=1800.00, stock=85, category_id=makeup.id, image_url="https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=400"),
        Product(name="Eyeshadow Palette", description="12-color eyeshadow palette", price=2900.00, stock=50, category_id=makeup.id, image_url="https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400"),
        Product(name="Blush", description="Natural glow blush", price=1400.00, stock=65, category_id=makeup.id, image_url="https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=400"),
        Product(name="Eyeliner", description="Waterproof eyeliner", price=1200.00, stock=90, category_id=makeup.id, image_url="https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=400"),
        Product(name="Lip Gloss", description="Shiny lip gloss", price=999.00, stock=110, category_id=makeup.id, image_url="https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400"),
        Product(name="Setting Spray", description="Long-lasting setting spray", price=2200.00, stock=55, category_id=makeup.id, image_url="https://images.unsplash.com/photo-1571875257727-256c39da42af?w=400"),
        
        # Haircare - 8 products
        Product(name="Shampoo", description="Nourishing shampoo", price=1299.00, stock=80, category_id=haircare.id, image_url="https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400"),
        Product(name="Conditioner", description="Deep conditioning treatment", price=1499.00, stock=75, category_id=haircare.id, image_url="https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400"),
        Product(name="Hair Oil", description="Argan hair oil", price=2500.00, stock=60, category_id=haircare.id, image_url="https://images.unsplash.com/photo-1571875257727-256c39da42af?w=400"),
        Product(name="Hair Mask", description="Repair hair mask", price=1800.00, stock=50, category_id=haircare.id, image_url="https://images.unsplash.com/photo-1629198688000-71f23e745b6e?w=400"),
        Product(name="Leave-in Conditioner", description="Moisturizing leave-in", price=1600.00, stock=70, category_id=haircare.id, image_url="https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400"),
        Product(name="Hair Serum", description="Smoothing hair serum", price=2200.00, stock=55, category_id=haircare.id, image_url="https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400"),
        Product(name="Dry Shampoo", description="Refreshing dry shampoo", price=1400.00, stock=65, category_id=haircare.id, image_url="https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400"),
        Product(name="Hair Spray", description="Strong hold hair spray", price=1100.00, stock=85, category_id=haircare.id, image_url="https://images.unsplash.com/photo-1571875257727-256c39da42af?w=400"),
    ]
    
    db.session.add_all(products)
    db.session.commit()
    
    print("✅ Database seeded successfully!")
    print(f"Created {Category.query.count()} categories")
    print(f"Created {Product.query.count()} products")
