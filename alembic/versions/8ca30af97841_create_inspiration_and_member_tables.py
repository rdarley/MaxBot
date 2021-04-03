"""Create Inspiration and Member tables

Revision ID: 8ca30af97841
Revises: 
Create Date: 2021-04-03 14:13:59.827588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ca30af97841'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'member',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('server', sa.String(50), nullable=False)
    )
    op.create_table(        
        'inspiration',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('server', sa.String(50), nullable=False),
        sa.Column('url', sa.String(200), nullable=False),
        sa.Column('member_id', sa.Integer, sa.ForeignKey('member.id'))
    )


def downgrade():
    pass
