"""Add phone and volunteer ID fields to users

Revision ID: a18c43d90f12
Revises: 291e42b3cf8b
Create Date: 2026-10-30 15:20:00

"""
from alembic import op
import sqlalchemy as sa


revision = "a18c43d90f12"
down_revision = "291e42b3cf8b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("phone", sa.String(length=30), nullable=True))
    op.add_column("users", sa.Column("volunteer_id", sa.String(length=80), nullable=True))
    op.create_unique_constraint("uq_users_volunteer_id", "users", ["volunteer_id"])


def downgrade():
    op.drop_constraint("uq_users_volunteer_id", "users", type_="unique")
    op.drop_column("users", "volunteer_id")
    op.drop_column("users", "phone")
