import uuid
from app.models.invoice import Invoice
from app.extensions import db

class InvoiceService:
    @staticmethod
    def create_invoice(order):
        invoice = Invoice(
            order_id=order.id,
            invoice_number=str(uuid.uuid4()),
            amount=order.total_price,
            status="PAID"
        )
        db.session.add(invoice)
        db.session.commit()
        return invoice
