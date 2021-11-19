"""add users table

Revision ID: 8fb24b2b62c8
Revises: b1e5ecbc46fb
Create Date: 2021-11-19 14:36:39.955223

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '8fb24b2b62c8'
down_revision = 'b1e5ecbc46fb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
