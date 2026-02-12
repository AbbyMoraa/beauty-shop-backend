from app.models.invoice import Invoice
from models import db
import uuid

class InvoiceService:
    @staticmethod
    def create_invoice(order):
        # check if invoice already exists
        existing = Invoice.query.filter_by(order_id=order.id).first()
        if existing:
            return existing
        
        inv_num = f"INV-{str(uuid.uuid4())[:8].upper()}"
        invoice = Invoice(
            order_id=order.id,
            invoice_number=inv_num,
            amount=order.total_price,
            status="PAID"
        )
        db.session.add(invoice)
        db.session.commit()
        return invoice
