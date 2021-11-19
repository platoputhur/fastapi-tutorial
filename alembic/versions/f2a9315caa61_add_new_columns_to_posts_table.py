"""add new columns to posts table

Revision ID: f2a9315caa61
Revises: a0d68da863b1
Create Date: 2021-11-19 15:08:15.808720

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f2a9315caa61'
down_revision = 'a0d68da863b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
                  )


pass


def downgrade():
    op.drop_column(column_name='published', table_name='posts')
    op.drop_column(column_name='created_at', table_name='posts')
    pass
