"""change password column type in users table

Revision ID: 1c0dd93d7de6
Revises: d32e96ec445d
Create Date: 2021-11-20 01:50:57.915958

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import Text, String

revision = '1c0dd93d7de6'
down_revision = 'd32e96ec445d'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("users", "password", type_=Text)
    pass


def downgrade():
    op.alter_column("users", "password", type_=String)
    pass
