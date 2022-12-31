"""empty message

Revision ID: 117ac9477925
Revises: 1f0b1c9e3fca
Create Date: 2022-12-30 16:04:07.684362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '117ac9477925'
down_revision = '1f0b1c9e3fca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=True))

    with op.batch_alter_table('seller', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seller', schema=None) as batch_op:
        batch_op.drop_column('status')

    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
