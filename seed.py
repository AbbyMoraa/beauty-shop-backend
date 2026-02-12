from flask import Flask
from models import db, Category, Product
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://ahmed:ahmed123@localhost/beauty_shop")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def seed_products():
    with app.app_context():
        # Clear existing data
        Product.query.delete()
        Category.query.delete()
        
        # Define categories and their products (10 each)
        categories_data = {
            "Skincare": [
                {"name": "Hydrating Face Serum", "description": "Deeply moisturizing serum with hyaluronic acid", "price": 4599.00, "stock": 50, "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400"},
                {"name": "Vitamin C Brightening Cream", "description": "Brightens and evens skin tone", "price": 3850.00, "stock": 40, "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400"},
                {"name": "Gentle Foaming Cleanser", "description": "Removes impurities without stripping skin", "price": 2200.00, "stock": 60, "image": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400"},
                {"name": "Night Repair Moisturizer", "description": "Intensive overnight hydration", "price": 5200.00, "stock": 35, "image": "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400"},
                {"name": "Exfoliating Toner", "description": "Refines pores and smooths texture", "price": 2899.00, "stock": 45, "image": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400"},
                {"name": "Face Cream", "description": "Moisturizing face cream", "price": 2599.00, "stock": 50, "image": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400"},
                {"name": "Eye Cream", "description": "Anti-wrinkle eye cream", "price": 3200.00, "stock": 35, "image": "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400"},
                {"name": "Sunscreen SPF 50", "description": "Broad spectrum sun protection", "price": 2800.00, "stock": 70, "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400"},
                {"name": "Retinol Night Serum", "description": "Anti-aging retinol treatment", "price": 5500.00, "stock": 30, "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400"},
                {"name": "Hydrating Face Mask", "description": "Intensive moisture boost", "price": 1800.00, "stock": 55, "image": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400"}
            ],
            "Makeup": [
                {"name": "Matte Liquid Lipstick", "description": "Long-lasting matte finish in berry shade", "price": 1899.00, "stock": 80, "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400"},
                {"name": "HD Foundation", "description": "Full coverage, natural finish", "price": 4200.00, "stock": 55, "image": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400"},
                {"name": "Volumizing Mascara", "description": "Dramatic lashes without clumping", "price": 2450.00, "stock": 70, "image": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=400"},
                {"name": "Eyeshadow Palette", "description": "12 versatile neutral shades", "price": 4800.00, "stock": 40, "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400"},
                {"name": "Cream Blush Stick", "description": "Buildable, dewy finish", "price": 1999.00, "stock": 65, "image": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400"},
                {"name": "Waterproof Eyeliner", "description": "Precision tip, smudge-proof", "price": 1500.00, "stock": 90, "image": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=400"},
                {"name": "Glossy Lip Gloss", "description": "High shine, non-sticky formula", "price": 1599.00, "stock": 110, "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400"},
                {"name": "Setting Spray", "description": "Long-lasting makeup hold", "price": 2200.00, "stock": 55, "image": "https://images.unsplash.com/photo-1571875257727-256c39da42af?w=400"},
                {"name": "Concealer Stick", "description": "Full coverage concealer", "price": 2100.00, "stock": 75, "image": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400"},
                {"name": "Brow Pencil", "description": "Natural-looking brow definition", "price": 1400.00, "stock": 85, "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400"}
            ],
            "Haircare": [
                {"name": "Repairing Hair Mask", "description": "Deep conditioning treatment for damaged hair", "price": 3200.00, "stock": 50, "image": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400"},
                {"name": "Volumizing Shampoo", "description": "Adds body and bounce", "price": 2650.00, "stock": 60, "image": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=400"},
                {"name": "Smoothing Conditioner", "description": "Tames frizz and adds shine", "price": 2650.00, "stock": 60, "image": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400"},
                {"name": "Heat Protection Spray", "description": "Shields hair from styling damage", "price": 2199.00, "stock": 55, "image": "https://images.unsplash.com/photo-1571875257727-256c39da42af?w=400"},
                {"name": "Argan Oil Hair Serum", "description": "Nourishes and adds gloss", "price": 2999.00, "stock": 45, "image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400"},
                {"name": "Leave-in Conditioner", "description": "Moisturizing leave-in treatment", "price": 1600.00, "stock": 70, "image": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400"},
                {"name": "Dry Shampoo", "description": "Refreshing dry shampoo", "price": 1800.00, "stock": 65, "image": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400"},
                {"name": "Strong Hold Hair Spray", "description": "All-day hold without stiffness", "price": 1500.00, "stock": 85, "image": "https://images.unsplash.com/photo-1571875257727-256c39da42af?w=400"},
                {"name": "Curl Defining Cream", "description": "Enhances natural curls", "price": 2400.00, "stock": 50, "image": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400"},
                {"name": "Scalp Treatment Oil", "description": "Nourishes scalp and promotes growth", "price": 2800.00, "stock": 40, "image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400"}
            ],
            "Fragrance": [
                {"name": "Floral Eau de Parfum", "description": "Elegant blend of rose and jasmine", "price": 7800.00, "stock": 30, "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400"},
                {"name": "Citrus Body Mist", "description": "Refreshing and light everyday scent", "price": 2499.00, "stock": 50, "image": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=400"},
                {"name": "Woody Cologne", "description": "Warm notes of sandalwood and cedar", "price": 8500.00, "stock": 25, "image": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=400"},
                {"name": "Vanilla Perfume Oil", "description": "Sweet and long-lasting roll-on", "price": 3200.00, "stock": 40, "image": "https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=400"},
                {"name": "Ocean Breeze Spray", "description": "Fresh aquatic fragrance", "price": 2850.00, "stock": 45, "image": "https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=400"},
                {"name": "Lavender Mist", "description": "Calming lavender scent", "price": 2200.00, "stock": 55, "image": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=400"},
                {"name": "Amber Perfume", "description": "Rich oriental fragrance", "price": 6500.00, "stock": 35, "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400"},
                {"name": "Rose Garden Spray", "description": "Romantic rose scent", "price": 3100.00, "stock": 48, "image": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=400"},
                {"name": "Musk Cologne", "description": "Sensual musk fragrance", "price": 7200.00, "stock": 28, "image": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=400"},
                {"name": "Tropical Paradise Mist", "description": "Exotic fruity fragrance", "price": 2600.00, "stock": 52, "image": "https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=400"}
            ],
            "Body Care": [
                {"name": "Shea Butter Body Lotion", "description": "Rich hydration for dry skin", "price": 1899.00, "stock": 70, "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400"},
                {"name": "Exfoliating Body Scrub", "description": "Buffs away dead skin cells", "price": 2400.00, "stock": 55, "image": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400"},
                {"name": "Luxury Bath Oil", "description": "Transforms bath into spa experience", "price": 3499.00, "stock": 35, "image": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400"},
                {"name": "Firming Body Cream", "description": "Improves skin elasticity", "price": 4200.00, "stock": 40, "image": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400"},
                {"name": "Soothing Hand Cream", "description": "Non-greasy, fast-absorbing formula", "price": 1799.00, "stock": 80, "image": "https://images.unsplash.com/photo-1585652757173-57de5e9fab42?w=400"},
                {"name": "Body Butter", "description": "Ultra-rich moisturizer", "price": 2900.00, "stock": 45, "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400"},
                {"name": "Shower Gel", "description": "Refreshing cleansing gel", "price": 1500.00, "stock": 90, "image": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400"},
                {"name": "Body Oil Spray", "description": "Lightweight hydrating oil", "price": 2700.00, "stock": 50, "image": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400"},
                {"name": "Foot Cream", "description": "Intensive foot care treatment", "price": 1600.00, "stock": 65, "image": "https://images.unsplash.com/photo-1585652757173-57de5e9fab42?w=400"},
                {"name": "Body Wash", "description": "Gentle cleansing body wash", "price": 1400.00, "stock": 75, "image": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400"}
            ]
        }

        # Create categories and products
        for category_name, products in categories_data.items():
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name, description=f"{category_name} products")
                db.session.add(category)
                db.session.flush()
            
            for product_data in products:
                existing = Product.query.filter_by(name=product_data["name"], category_id=category.id).first()
                if not existing:
                    product = Product(
                        name=product_data["name"],
                        description=product_data["description"],
                        price=product_data["price"],
                        stock=product_data["stock"],
                        category_id=category.id,
                        image_url=product_data["image"]
                    )
                    db.session.add(product)
        
        db.session.commit()
        print("✅ Successfully seeded products!")
        print(f"Created {Category.query.count()} categories")
        print(f"Created {Product.query.count()} products")

if __name__ == "__main__":
    seed_products()
