from app.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_ref = db.Column(db.String(100), unique=True, nullable=True)
    payment_status = db.Column(db.String(20), default="PENDING")

    items = db.relationship("OrderItem", backref="order", lazy=True)
    invoice = db.relationship("Invoice", backref="order", lazy=True, uselist=False)
