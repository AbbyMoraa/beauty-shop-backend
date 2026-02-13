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
    {'id': 4, 'customer': 'Sarah Wilson', 'total': 75.25, 'status': 'Shipped', 'date': '2024-01-28', 'category': 'Skincare'},
]

mock_users = [
    {'id': 1, 'name': 'Alice Brown', 'email': 'alice@example.com', 'role': 'customer', 'status': 'active'},
    {'id': 2, 'name': 'Charlie Davis', 'email': 'charlie@example.com', 'role': 'admin', 'status': 'active'},
    {'id': 3, 'name': 'Mike Johnson', 'email': 'mike@test.com', 'role': 'customer', 'status': 'active'},
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
    
    filtered_orders = mock_orders.copy()
    
    if date_filter:
        filtered_orders = [order for order in filtered_orders if order['date'] == date_filter]
    if category_filter:
        filtered_orders = [order for order in filtered_orders if order['category'] == category_filter]
    
    return jsonify({
        'orders': filtered_orders,
        'total': len(filtered_orders)
    }), 200

@admin_bp.route('/analytics/products', methods=['GET'])
@jwt_required()
def get_product_analytics():
    return jsonify({
        'products': mock_products,
        'message': 'Product analytics data'
    }), 200

@admin_bp.route('/analytics/orders', methods=['GET'])
@jwt_required()
def get_order_analytics():
    total_orders = len(mock_orders)
    total_revenue = sum(order['total'] for order in mock_orders)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    pending_count = 0
    for order in mock_orders:
        if order['status'] == 'Pending':
            pending_count += 1
    
    analytics_data = {
        'totalOrders': total_orders,
        'totalRevenue': round(total_revenue, 2),
        'averageOrderValue': round(avg_order_value, 2),
        'pendingOrders': pending_count,
        'completedOrders': len([o for o in mock_orders if o['status'] == 'Completed'])
    }
    
    return jsonify(analytics_data), 200

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    return jsonify({
        'users': mock_users,
        'count': len(mock_users)
    }), 200

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.json
    
    user_found = None
    for i, user in enumerate(mock_users):
        if user['id'] == user_id:
            user_found = user
            break
    
    if not user_found:
        return jsonify({'error': 'User not found'}), 404
    
    if 'role' in data:
        user_found['role'] = data['role']
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user_found
    }), 200

@admin_bp.route('/users/<int:user_id>/disable', methods=['POST'])
@jwt_required()
def disable_user(user_id):
    for user in mock_users:
        if user['id'] == user_id:
            user['status'] = 'disabled'
            return jsonify({
                'message': f'User {user["name"]} has been disabled',
                'user': user
            }), 200
    
    return jsonify({'error': 'User not found'}), 404

@admin_bp.route('/export/orders', methods=['GET'])
@jwt_required()
def export_orders():
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Order ID', 'Customer Name', 'Total Amount', 'Status', 'Order Date', 'Category'])
    
    for order in mock_orders:
        writer.writerow([
            order['id'],
            order['customer'],
            f"${order['total']:.2f}",
            order['status'],
            order['date'],
            order['category']
        ])
    
    csv_data = output.getvalue()
    output.close()
    
    response = make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=beauty_shop_orders.csv'
    
    return response

@admin_bp.route('/export/orders/pdf', methods=['GET'])
@jwt_required()
def export_orders_pdf():
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    
    pdf_canvas.setFont('Helvetica-Bold', 18)
    pdf_canvas.drawString(50, 750, 'Beauty Shop - Orders Report')
    
    from datetime import datetime
    pdf_canvas.setFont('Helvetica', 10)
    pdf_canvas.drawString(50, 730, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    
    pdf_canvas.setFont('Helvetica-Bold', 10)
    y_position = 680
    pdf_canvas.drawString(50, y_position, 'ID')
    pdf_canvas.drawString(100, y_position, 'Customer')
    pdf_canvas.drawString(250, y_position, 'Total')
    pdf_canvas.drawString(320, y_position, 'Status')
    pdf_canvas.drawString(400, y_position, 'Date')
    pdf_canvas.drawString(480, y_position, 'Category')
    
    pdf_canvas.line(50, y_position-5, 550, y_position-5)
    
    pdf_canvas.setFont('Helvetica', 9)
    y_position -= 25
    
    for order in mock_orders:
        pdf_canvas.drawString(50, y_position, str(order['id']))
        pdf_canvas.drawString(100, y_position, order['customer'])
        pdf_canvas.drawString(250, y_position, f"${order['total']:.2f}")
        pdf_canvas.drawString(320, y_position, order['status'])
        pdf_canvas.drawString(400, y_position, order['date'])
        pdf_canvas.drawString(480, y_position, order['category'])
        y_position -= 20
        
        if y_position < 100:
            pdf_canvas.showPage()
            y_position = 750
    
    pdf_canvas.save()
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=beauty_shop_orders_report.pdf'
    
    return response
