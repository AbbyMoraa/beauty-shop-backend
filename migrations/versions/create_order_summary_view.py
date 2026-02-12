"""Create order_summary view

Revision ID: create_order_summary_view
Revises: 
Create Date: 2024-01-15

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_order_summary_view'
down_revision = None  # Update this to your latest migration
branch_label = None
depends_on = None


def upgrade():
    # Create the order_summary view
    op.execute("""
        CREATE VIEW order_summary AS
        SELECT 
            o.id AS order_id,
            o.user_id,
            u.email AS user_email,
            o.total_price,
            o.status,
            o.payment_status,
            o.created_at,
            COUNT(oi.id) AS total_items
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.id
        LEFT JOIN order_items oi ON o.id = oi.order_id
        GROUP BY o.id, o.user_id, u.email, o.total_price, o.status, o.payment_status, o.created_at
    """)


def downgrade():
    # Drop the order_summary view
    op.execute("DROP VIEW IF EXISTS order_summary")
