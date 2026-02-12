from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import csv
from io import StringIO, BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
mock_orders = [
    {'id': 1, 'customer': 'John Doe', 'total': 150.00, 'status': 'Completed', 'date': '2024-01-15', 'category': 'Skincare'},
    {'id': 2, 'customer': 'Jane Smith', 'total': 89.99, 'status': 'Pending', 'date': '2024-01-20', 'category': 'Makeup'},
    {'id': 3, 'customer': 'Bob Johnson', 'total': 200.50, 'status': 'Completed', 'date': '2024-02-01', 'category': 'Haircare'},
]

mock_users = [
    {'id': 1, 'name': 'Alice Brown', 'email': 'alice@example.com', 'role': 'customer', 'status': 'active'},
    {'id': 2, 'name': 'Charlie Davis', 'email': 'charlie@example.com', 'role': 'admin', 'status': 'active'},
]

mock_products = [
    {'id': 1, 'name': 'Face Cream', 'sales': 45, 'revenue': 2250.00, 'views': 320},
    {'id': 2, 'name': 'Lipstick', 'sales': 67, 'revenue': 1340.00, 'views': 450},
    {'id': 3, 'name': 'Shampoo', 'sales': 89, 'revenue': 1780.00, 'views': 520},
]

@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    date_filter = request.args.get('date')
    category_filter = request.args.get('category')
    
    filtered_orders = mock_orders
    
    if date_filter:
        filtered_orders = [o for o in filtered_orders if o['date'] == date_filter]
    if category_filter:
        filtered_orders = [o for o in filtered_orders if o['category'] == category_filter]
    
    return jsonify(filtered_orders), 200

@admin_bp.route('/analytics/products', methods=['GET'])
@jwt_required()
def get_product_analytics():
    return jsonify(mock_products), 200

@admin_bp.route('/analytics/orders', methods=['GET'])
@jwt_required()
def get_order_analytics():
    total_orders = len(mock_orders)
    total_revenue = sum(o['total'] for o in mock_orders)
    avg_order = total_revenue / total_orders if total_orders > 0 else 0
    
    analytics = {
        'totalOrders': total_orders,
        'totalRevenue': total_revenue,
        'averageOrder': avg_order,
        'pendingOrders': len([o for o in mock_orders if o['status'] == 'Pending'])
    }
    
    return jsonify(analytics), 200

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    return jsonify(mock_users), 200

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.json
    for user in mock_users:
        if user['id'] == user_id:
            user['role'] = data.get('role', user['role'])
            return jsonify({'message': 'User updated', 'user': user}), 200
    
    return jsonify({'error': 'User not found'}), 404

@admin_bp.route('/users/<int:user_id>/disable', methods=['POST'])
@jwt_required()
def disable_user(user_id):
    for user in mock_users:
        if user['id'] == user_id:
            user['status'] = 'disabled'
            return jsonify({'message': 'User disabled', 'user': user}), 200
    
    return jsonify({'error': 'User not found'}), 404

@admin_bp.route('/export/orders', methods=['GET'])
@jwt_required()
def export_orders():
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Customer', 'Total', 'Status', 'Date', 'Category'])
    
    for order in mock_orders:
        writer.writerow([
            order['id'],
            order['customer'],
            order['total'],
            order['status'],
            order['date'],
            order['category']
        ])
    
    csv_content = output.getvalue()
    output.close()
    
    return csv_content, 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=orders.csv'
    }

@admin_bp.route('/export/orders/pdf', methods=['GET'])
@jwt_required()
def export_orders_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(50, 750, 'Beauty Shop - Orders Report')
    
    pdf.setFont('Helvetica-Bold', 10)
    y = 700
    pdf.drawString(50, y, 'ID')
    pdf.drawString(100, y, 'Customer')
    pdf.drawString(250, y, 'Total')
    pdf.drawString(320, y, 'Status')
    pdf.drawString(400, y, 'Date')
    pdf.drawString(480, y, 'Category')
    
    pdf.setFont('Helvetica', 10)
    y -= 20
    for order in mock_orders:
        pdf.drawString(50, y, str(order['id']))
        pdf.drawString(100, y, order['customer'])
        pdf.drawString(250, y, f"${order['total']}")
        pdf.drawString(320, y, order['status'])
        pdf.drawString(400, y, order['date'])
        pdf.drawString(480, y, order['category'])
        y -= 20
    
    pdf.save()
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=orders.pdf'
    
    return response
