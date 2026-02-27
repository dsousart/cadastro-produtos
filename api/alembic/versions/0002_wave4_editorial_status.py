"""wave4 add editorial product statuses

Revision ID: 0002_wave4_editorial_status
Revises: 0001_wave1_initial
Create Date: 2026-02-27
"""

from alembic import op


revision = "0002_wave4_editorial_status"
down_revision = "0001_wave1_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE product_status ADD VALUE IF NOT EXISTS 'in_review';")
    op.execute("ALTER TYPE product_status ADD VALUE IF NOT EXISTS 'rejected';")


def downgrade() -> None:
    # PostgreSQL enum value removal is not safe without type recreation.
    pass
