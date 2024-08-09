"""Add purchase_date to cart

Revision ID: a6ba66e797a1
Revises: f4c8633a416f
Create Date: 2024-07-28 15:06:37.611320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6ba66e797a1'
down_revision = 'f4c8633a416f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('purchase_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.drop_column('purchase_date')

    # ### end Alembic commands ###
