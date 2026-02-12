from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask_swagger_ui import get_swaggerui_blueprint
from models import db, User, Product, CartItem, Order, OrderItem
from app.routes.product_routes import product_bp
from app.routes.payment_routes import payment_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///beauty_shop.db")
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

@app.route("/")
def home():
    return jsonify({
        "message": "Beauty Shop API",
        "docs": "/docs",
        "endpoints": {
            "products": "/products",
            "categories": "/categories",
            "cart": "/cart",
            "checkout": "/checkout",
            "auth": {
                "register": "/register",
                "login": "/login"
            }
        }
    })

@app.route("/swagger.json")
def swagger_spec():
    with open('swagger.json', 'r') as f:
        import json
        return jsonify(json.load(f))

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username") or data.get("email")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "missing username or password"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "user already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username") or data.get("email")
    password = data.get("password")
    
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "wrong username or password"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200


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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
