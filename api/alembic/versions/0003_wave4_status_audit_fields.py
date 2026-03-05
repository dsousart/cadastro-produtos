"""wave4 add status audit fields on products

Revision ID: 0003_wave4_status_audit_fields
Revises: 0002_wave4_editorial_status
Create Date: 2026-02-27
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_wave4_status_audit_fields"
down_revision = "0002_wave4_editorial_status"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("products", sa.Column("status_updated_by", sa.String(length=120), nullable=True))
    op.add_column("products", sa.Column("status_updated_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("products", "status_updated_at")
    op.drop_column("products", "status_updated_by")
