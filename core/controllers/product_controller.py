from flask import jsonify, request
from models import Product, Category, db

class ProductController:
    
    @staticmethod
    def get_all_products():
        category_id = request.args.get('category_id')
        search = request.args.get('search')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        query = Product.query
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        
        if min_price:
            query = query.filter(Product.price >= min_price)
        
        if max_price:
            query = query.filter(Product.price <= max_price)
        
        products = query.all()
        return jsonify([p.to_dict() for p in products]), 200
    
    @staticmethod
    def get_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product.to_dict()), 200
    
    @staticmethod
    def create_product():
        data = request.get_json()
        product = Product(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            image_url=data.get('image_url'),
            stock=data.get('stock', 0),
            category_id=data.get('category_id')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    
    @staticmethod
    def update_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        data = request.get_json()
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.image_url = data.get('image_url', product.image_url)
        product.stock = data.get('stock', product.stock)
        product.category_id = data.get('category_id', product.category_id)
        
        db.session.commit()
        return jsonify(product.to_dict()), 200
    
    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'}), 200
    
    @staticmethod
    def get_all_categories():
        categories = Category.query.all()
        return jsonify([c.to_dict() for c in categories]), 200
    
    @staticmethod
    def get_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        return jsonify(category.to_dict()), 200
    
    @staticmethod
    def create_category():
        data = request.get_json()
        category = Category(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(category)
        db.session.commit()
        return jsonify(category.to_dict()), 201
