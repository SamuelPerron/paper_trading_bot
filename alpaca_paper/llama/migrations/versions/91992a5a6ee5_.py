"""empty message

Revision ID: 91992a5a6ee5
Revises: 2206315bf987
Create Date: 2021-04-18 17:27:53.692070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91992a5a6ee5'
down_revision = '2206315bf987'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association_account_orders',
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association_account_orders')
    # ### end Alembic commands ###
