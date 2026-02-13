from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask_swagger_ui import get_swaggerui_blueprint
from models import db, User, Product, CartItem, Order, OrderItem, Category
from app.routes.product_routes import product_bp
from app.routes.payment_routes import payment_bp
from admin.routes.admin_routes import admin_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://ahmed:ahmed123@localhost/beauty_shop")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
jwt = JWTManager(app)

# Swagger UI setup
SWAGGER_URL = '/docs'
API_URL = '/swagger.json'
swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Beauty Shop API"}
)
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

# Register blueprints
app.register_blueprint(product_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(admin_bp)

@app.route("/")
def home():
    return jsonify({
        "message": "Beauty Shop API",
        "docs": "/docs",
        "endpoints": {
            "products": "/products",
            "admin": "/admin",
            "auth": {
                "register": "/register",
                "login": "/login"
            },
            "cart": "/cart",
            "checkout": "/checkout"
        }
    })

@app.route("/swagger.json")
def swagger_spec():
    with open('swagger.json', 'r') as f:
        import json
        return jsonify(json.load(f))

@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict())

@app.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username") or (email.split("@")[0] if email else None)
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "missing username or password"}), 400

    if email and User.query.filter_by(email=email).first():
        return jsonify({"error": "email already exists"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "user already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    
    user = None
    if email:
        user = User.query.filter_by(email=email).first()
    elif username:
        user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({"error": "wrong username or password"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": token,
        "username": user.username,
        "role": user.role,
        "user_id": user.id
    }), 200

@app.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "name": user.username,
        "email": user.email,
        "role": user.role
    }), 200

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "role": u.role,
        "created_at": str(u.created_at)
    } for u in users])

@app.route("/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

@app.route("/cart", methods=["GET"])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=user_id).all()
    cart = []
    for i in items:
        product = Product.query.get(i.product_id)
        cart.append({
            "product_id": i.product_id,
            "quantity": i.quantity,
            "product_name": product.name,
            "price": product.price
        })
    return jsonify(cart)

@app.route("/cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    item = CartItem(
        user_id=user_id, 
        product_id=data["product_id"], 
        quantity=data.get("quantity", 1)
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "added to cart"}), 201

@app.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    if not cart_items:
        return jsonify({"error": "cart is empty"}), 400

    order = Order(user_id=user_id, total_price=0)
    db.session.add(order)
    db.session.flush()

    total = 0
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if not product:
            continue
        total += product.price * item.quantity
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        )
        db.session.add(order_item)

    order.total_price = total
    db.session.commit()

    # clear cart
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return jsonify({"message": "checkout complete", "order_id": order.id, "total": total}), 201

@app.route("/orders", methods=["GET"])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": o.id,
        "total_price": o.total_price,
        "status": o.status,
        "created_at": str(o.created_at),
        "items": [{
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": item.unit_price
        } for item in o.items]
    } for o in orders])

@app.route("/analytics/products", methods=["GET"])
@jwt_required()
def analytics_products():
    from sqlalchemy import func
    products = db.session.query(
        Product.id, Product.name,
        func.count(OrderItem.id).label('sales'),
        func.sum(OrderItem.quantity * OrderItem.unit_price).label('revenue')
    ).join(OrderItem).group_by(Product.id).all()
    
    return jsonify([{
        'id': p.id, 'name': p.name, 'sales': p.sales, 'revenue': float(p.revenue or 0)
    } for p in products])

@app.route("/analytics/orders", methods=["GET"])
@jwt_required()
def analytics_orders():
    from sqlalchemy import func
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_price)).scalar() or 0
    pending = Order.query.filter_by(status='pending').count()
    
    return jsonify({
        'totalOrders': total_orders,
        'totalRevenue': float(total_revenue),
        'averageOrder': float(total_revenue / total_orders) if total_orders > 0 else 0,
        'pendingOrders': pending
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
