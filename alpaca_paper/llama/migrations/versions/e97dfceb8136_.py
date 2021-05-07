"""empty message

Revision ID: e97dfceb8136
Revises: 913ce0b5d356
Create Date: 2021-05-07 03:51:00.702798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e97dfceb8136'
down_revision = '913ce0b5d356'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('rejected_cause', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'rejected_cause')
    # ### end Alembic commands ###
