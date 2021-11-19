"""add content column to posts table

Revision ID: b1e5ecbc46fb
Revises: ed8b34532efa
Create Date: 2021-11-19 13:59:29.636772

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b1e5ecbc46fb'
down_revision = 'ed8b34532efa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
