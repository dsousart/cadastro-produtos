"""wave1 initial schema

Revision ID: 0001_wave1_initial
Revises:
Create Date: 2026-02-26
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0001_wave1_initial"
down_revision = None
branch_labels = None
depends_on = None


product_status_enum = sa.Enum(
    "draft",
    "generated",
    "approved",
    "published",
    name="product_status",
)

job_status_enum = sa.Enum(
    "pending",
    "running",
    "completed",
    "failed",
    name="generation_job_status",
)

user_role_enum = sa.Enum("admin", "editor", "viewer", name="user_role")


def upgrade() -> None:
    bind = op.get_bind()
    product_status_enum.create(bind, checkfirst=True)
    job_status_enum.create(bind, checkfirst=True)
    user_role_enum.create(bind, checkfirst=True)

    op.create_table(
        "tenants",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("slug", sa.String(length=120), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_tenants_slug", "tenants", ["slug"], unique=True)

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id"), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            postgresql.ENUM("admin", "editor", "viewer", name="user_role", create_type=False),
            nullable=False,
            server_default="viewer",
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_tenant_id", "users", ["tenant_id"], unique=False)

    op.create_table(
        "generation_jobs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id"), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM(
                "pending",
                "running",
                "completed",
                "failed",
                name="generation_job_status",
                create_type=False,
            ),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("total_items", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("completed_items", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed_items", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("request_payload", sa.JSON(), nullable=True),
        sa.Column("result_payload", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_generation_jobs_tenant_id", "generation_jobs", ["tenant_id"], unique=False)
    op.create_index("ix_generation_jobs_status", "generation_jobs", ["status"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id"), nullable=True),
        sa.Column("generation_job_id", sa.String(length=36), sa.ForeignKey("generation_jobs.id"), nullable=True),
        sa.Column("sku", sa.String(length=120), nullable=False),
        sa.Column("nome_produto", sa.String(length=255), nullable=False),
        sa.Column("marca", sa.String(length=255), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "draft",
                "generated",
                "approved",
                "published",
                name="product_status",
                create_type=False,
            ),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("score_qualidade", sa.Integer(), nullable=True),
        sa.Column("input_payload", sa.JSON(), nullable=False),
        sa.Column("output_payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_products_tenant_id", "products", ["tenant_id"], unique=False)
    op.create_index("ix_products_status", "products", ["status"], unique=False)
    op.create_index("ix_products_sku", "products", ["sku"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_products_sku", table_name="products")
    op.drop_index("ix_products_status", table_name="products")
    op.drop_index("ix_products_tenant_id", table_name="products")
    op.drop_table("products")

    op.drop_index("ix_generation_jobs_status", table_name="generation_jobs")
    op.drop_index("ix_generation_jobs_tenant_id", table_name="generation_jobs")
    op.drop_table("generation_jobs")

    op.drop_index("ix_users_tenant_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_tenants_slug", table_name="tenants")
    op.drop_table("tenants")

    bind = op.get_bind()
    product_status_enum.drop(bind, checkfirst=True)
    job_status_enum.drop(bind, checkfirst=True)
    user_role_enum.drop(bind, checkfirst=True)
