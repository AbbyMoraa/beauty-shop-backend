from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity, create_access_token
)

from models import db, User, Product, CartItem, Order, OrderItem

from app.routes.product_routes import product_bp
from admin.routes.admin_routes import admin_bp

app = Flask(__name__)
CORS(app)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ahmed:ahmed123@localhost/beauty_shop"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"

db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(product_bp)
app.register_blueprint(admin_bp)

# -------------------- HOME --------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Beauty Shop API Running",
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

# -------------------- AUTH --------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(username=data["username"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(
        username=data["username"],
        password=data["password"]
    ).first()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200

# -------------------- CART --------------------
@app.route("/cart", methods=["GET"])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "product_id": i.product_id,
            "quantity": i.quantity,
            "product_name": Product.query.get(i.product_id).name,
            "price": Product.query.get(i.product_id).price
        }
        for i in items
    ])

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

    return jsonify({"message": "Item added to cart"}), 201

# -------------------- CHECKOUT --------------------
@app.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    total = 0
    order = Order(user_id=user_id, total_price=0)
    db.session.add(order)
    db.session.flush()

    for item in cart_items:
        product = Product.query.get(item.product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        total += product.price * item.quantity
        db.session.add(OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        ))

    order.total_price = total
    db.session.commit()

    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return jsonify({
        "message": "Checkout successful",
        "order_id": order.id,
        "total": total
    }), 201

# -------------------- MAIN --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("\nRegistered routes:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule}")

    app.run(debug=True)
