"""create Admin,User tables

Revision ID: 949ead1f8c9e
Revises: acfea3d27eea
Create Date: 2016-12-08 05:29:26.654000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '949ead1f8c9e'
down_revision = 'acfea3d27eea'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'User',
        sa.Column(u'id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column(u'date_created', sa.DateTime(), nullable=False),
        sa.Column(u'date_modified', sa.DateTime(), nullable=False),
        sa.Column(u'email', sa.String(length=128), nullable=False, unique=True),
        sa.Column(u'name', sa.String(length=64)),
        sa.Column(u'password', sa.String(length=64), nullable=False),
        sa.Column(u'phone', sa.BigInteger()),
        sa.Column(u'username', sa.String(length=32), nullable=False, unique=True),

    )
    op.create_table(
        'Admin',
        sa.Column(u'id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column(u'date_created', sa.DateTime(), nullable=False),
        sa.Column(u'date_modified', sa.DateTime(), nullable=False),
        sa.Column(u'level', sa.String(length=8), nullable=False),
        sa.Column(u'user_id', sa.Integer(), sa.ForeignKey('User.id')),

    )
    op.create_table('products',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=64), nullable=True),
                    sa.Column('description', sa.String(length=300), nullable=True),
                    sa.Column('price', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('title')
                    )

def downgrade():
    pass
