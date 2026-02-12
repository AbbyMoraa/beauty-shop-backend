from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Order, db
from app.models.invoice import Invoice
from app.models.address import Address
from app.services.payment_service import PaydPaymentService
from app.services.invoice_service import InvoiceService
import os

payment_bp = Blueprint("payment_bp", __name__)

@payment_bp.route("/payments/initiate", methods=["POST"])
@jwt_required()
def initiate_payment():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    order_id = data.get("order_id")
    phone = data.get("phone_number")
    
    if not order_id or not phone:
        return jsonify({"error": "need order_id and phone_number"}), 400
    
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({"error": "order not found"}), 404
    
    if order.payment_status == "PAID":
        return jsonify({"error": "already paid"}), 400
    
    if not os.getenv('PAYD_API_USERNAME') or not os.getenv('PAYD_API_PASSWORD'):
        return jsonify({"error": "payment service not set up, use /payments/simulate instead"}), 503
    
    callback = f"{os.getenv('APP_URL', 'http://localhost:5000')}/payments/callback"
    
    try:
        response, status = PaydPaymentService.initiate_payment(
            amount=order.total_price,
            phone_number=phone,
            narration=f"Order #{order.id}",
            callback_url=callback,
            transaction_ref=order.transaction_ref
        )
        
        if status >= 400:
            return jsonify({"error": "payment failed, try /payments/simulate"}), 503
        
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": "payment service down"}), 503

@payment_bp.route("/payments/simulate", methods=["POST"])
@jwt_required()
def simulate_payment():
    user_id = get_jwt_identity()
    data = request.get_json()
    order_id = data.get("order_id")
    
    if not order_id:
        return jsonify({"error": "need order_id"}), 400
    
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({"error": "order not found"}), 404
    
    order.payment_status = "PAID"
    order.status = "confirmed"
    db.session.commit()
    
    invoice = InvoiceService.create_invoice(order)
    
    return jsonify({
        "message": "payment successful",
        "order_id": order.id,
        "payment_status": order.payment_status,
        "invoice_number": invoice.invoice_number
    }), 200

@payment_bp.route("/payments/callback", methods=["POST"])
def payd_webhook():
    data = request.get_json()
    ref = data.get("reference")
    status = data.get("status")

    if not ref:
        return jsonify({"error": "no reference"}), 400

    order = Order.query.filter_by(transaction_ref=ref).first()
    if not order:
        return jsonify({"error": "order not found"}), 404

    if status == "SUCCESS":
        order.payment_status = "PAID"
        order.status = "confirmed"
        InvoiceService.create_invoice(order)
    else:
        order.payment_status = "FAILED"
    
    db.session.commit()
    return jsonify({"message": "ok"}), 200

@payment_bp.route("/invoices/<int:order_id>", methods=["GET"])
@jwt_required()
def get_invoice(order_id):
    user_id = get_jwt_identity()
    
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({"error": "order not found"}), 404
    
    invoice = Invoice.query.filter_by(order_id=order.id).first()
    if not invoice:
        return jsonify({"error": "no invoice yet"}), 404
    
    items = []
    for item in order.items:
        items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": item.unit_price
        })
    
    return jsonify({
        "invoice_number": invoice.invoice_number,
        "order_id": invoice.order_id,
        "amount": invoice.amount,
        "status": invoice.status,
        "created_at": invoice.created_at.isoformat(),
        "order_details": {
            "transaction_ref": order.transaction_ref,
            "payment_status": order.payment_status,
            "items": items
        }
    }), 200

@payment_bp.route("/addresses", methods=["POST"])
@jwt_required()
def create_address():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required = ["full_name", "phone_number", "address_line", "city"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"missing {field}"}), 400
    
    address = Address(
        user_id=user_id,
        full_name=data.get("full_name"),
        phone_number=data.get("phone_number"),
        address_line=data.get("address_line"),
        city=data.get("city"),
        postal_code=data.get("postal_code"),
        address_type=data.get("address_type", "billing")
    )
    
    db.session.add(address)
    db.session.commit()
    
    return jsonify({"message": "address saved", "id": address.id}), 201

@payment_bp.route("/addresses", methods=["GET"])
@jwt_required()
def get_addresses():
    user_id = get_jwt_identity()
    addresses = Address.query.filter_by(user_id=user_id).all()
    
    result = []
    for addr in addresses:
        result.append({
            "id": addr.id,
            "full_name": addr.full_name,
            "phone_number": addr.phone_number,
            "address_line": addr.address_line,
            "city": addr.city,
            "postal_code": addr.postal_code,
            "address_type": addr.address_type
        })
    return jsonify(result), 200
