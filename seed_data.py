import sys
sys.path.insert(0, '.')
from models import db, Product, Category
from flask import Flask
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///beauty_shop.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    # Clear existing
    Product.query.delete()
    Category.query.delete()
    
    # Add categories
    skincare = Category(name='Skincare', description='Skincare products')
    makeup = Category(name='Makeup', description='Makeup products')
    haircare = Category(name='Haircare', description='Hair products')
    db.session.add_all([skincare, makeup, haircare])
    db.session.commit()
    
    # Add products
    products = [
        Product(name='Hydrating Face Cream', description='Deep moisturizing cream', price=25.99, stock=50, category_id=skincare.id, image_url='https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400'),
        Product(name='Vitamin C Serum', description='Brightening serum', price=35.99, stock=30, category_id=skincare.id, image_url='https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400'),
        Product(name='Sunscreen SPF 50', description='Daily sun protection', price=18.99, stock=60, category_id=skincare.id, image_url='https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'),
        Product(name='Matte Lipstick', description='Long-lasting matte finish', price=15.99, stock=100, category_id=makeup.id, image_url='https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400'),
        Product(name='Foundation', description='Full coverage foundation', price=29.99, stock=40, category_id=makeup.id, image_url='https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400'),
        Product(name='Mascara', description='Volumizing mascara', price=12.99, stock=80, category_id=makeup.id, image_url='https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=400'),
        Product(name='Shampoo', description='Nourishing shampoo', price=14.99, stock=70, category_id=haircare.id, image_url='https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400'),
        Product(name='Conditioner', description='Smoothing conditioner', price=14.99, stock=70, category_id=haircare.id, image_url='https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400'),
    ]
    db.session.add_all(products)
    db.session.commit()
    
    print(f'Added {len(products)} products and 3 categories')
