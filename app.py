from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from models import db, User, Product, CartItem, Order, OrderItem

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ahmed:ahmed123@localhost/beauty_shop"
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # change to something secure

db.init_app(app)
jwt = JWTManager(app)

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
    user = User.query.filter_by(username=data["username"], password=data["password"]).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200

# -------------------- PRODUCTS --------------------
@app.route("/products", methods=["GET"])
def list_products():
    products = Product.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price}
        for p in products
    ])

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
    product_id = data["product_id"]
    quantity = data.get("quantity", 1)

    item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
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
            return jsonify({"error": f"Product {item.product_id} not found"}), 404

        unit_price = product.price
        total += unit_price * item.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=unit_price
        )
        db.session.add(order_item)

    order.total_price = total
    db.session.commit()

    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return jsonify({"message": "Checkout successful", "order_id": order.id, "total": total}), 201

# -------------------- MAIN --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ensures tables exist if migrations already applied
    app.run()