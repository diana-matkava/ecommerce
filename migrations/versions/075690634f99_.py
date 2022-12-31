"""empty message

Revision ID: 075690634f99
Revises: 117ac9477925
Create Date: 2022-12-30 16:05:09.016934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '075690634f99'
down_revision = '117ac9477925'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('seller', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seller', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###
