from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from sqlalchemy import func, desc
from datetime import datetime, timedelta

class AnalyticsService:
    
    @staticmethod
    def get_product_sales_analytics(start_date=None, end_date=None):
        query = db.session.query(
            Product.id,
            Product.name,
            func.sum(OrderItem.quantity).label('total_sold'),
            func.sum(OrderItem.quantity * OrderItem.unit_price).label('total_revenue')
        ).join(OrderItem).join(Order)
        
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at <= end_date)
        
        results = query.group_by(Product.id, Product.name).order_by(desc('total_revenue')).all()
        
        return [{
            'product_id': r.id,
            'product_name': r.name,
            'total_sold': int(r.total_sold),
            'total_revenue': float(r.total_revenue)
        } for r in results]
    
    @staticmethod
    def get_order_analytics(start_date=None, end_date=None):
        query = db.session.query(Order)
        
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at <= end_date)
        
        total_orders = query.count()
        total_revenue = db.session.query(func.sum(Order.total_price)).filter(
            Order.created_at >= start_date if start_date else True,
            Order.created_at <= end_date if end_date else True
        ).scalar() or 0
        
        status_breakdown = db.session.query(
            Order.status,
            func.count(Order.id)
        ).filter(
            Order.created_at >= start_date if start_date else True,
            Order.created_at <= end_date if end_date else True
        ).group_by(Order.status).all()
        
        return {
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'status_breakdown': {status: count for status, count in status_breakdown}
        }
