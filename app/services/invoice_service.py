from app.models.invoice import Invoice
from models import db
import uuid

class InvoiceService:
    @staticmethod
    def create_invoice(order):
        existing = Invoice.query.filter_by(order_id=order.id).first()
        if existing:
            return existing
        
        invoice_number = f"INV-{str(uuid.uuid4())[:8].upper()}"
        invoice = Invoice(
            order_id=order.id,
            invoice_number=invoice_number,
            amount=order.total_price,
            status="PAID"
        )
        db.session.add(invoice)
        db.session.commit()
        return invoice
