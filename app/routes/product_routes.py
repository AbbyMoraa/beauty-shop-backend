from flask import Blueprint
from app.controllers.product_controller import ProductController

product_bp = Blueprint('products', __name__)

# Product routes
@product_bp.route('/products', methods=['GET'])
def get_products():
    return ProductController.get_all_products()

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return ProductController.get_product(product_id)

@product_bp.route('/products', methods=['POST'])
def create_product():
    return ProductController.create_product()

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return ProductController.update_product(product_id)

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return ProductController.delete_product(product_id)

# Category routes
@product_bp.route('/categories', methods=['GET'])
def get_categories():
    return ProductController.get_all_categories()

@product_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    return ProductController.get_category(category_id)

@product_bp.route('/categories', methods=['POST'])
def create_category():
    return ProductController.create_category()
