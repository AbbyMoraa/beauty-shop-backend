from app.extensions import db

class OrderSummary(db.Model):
    __tablename__ = 'order_summary'
    __table_args__ = {'info': dict(is_view=True)}
    
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_email = db.Column(db.String(120))
    total_price = db.Column(db.Float)
    status = db.Column(db.String(20))
    payment_status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)
    total_items = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'user_email': self.user_email,
            'total_price': self.total_price,
            'status': self.status,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'total_items': self.total_items
        }
