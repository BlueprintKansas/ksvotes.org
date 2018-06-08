"""empty message

Revision ID: 879fe8a73df4
Revises: 8c3766231a8f
Create Date: 2018-06-07 19:56:40.800424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '879fe8a73df4'
down_revision = '8c3766231a8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('registrants', sa.Column('addr_lookup_complete', sa.Boolean(), nullable=True))
    op.add_column('registrants', sa.Column('reg_lookup_complete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('registrants', 'reg_lookup_complete')
    op.drop_column('registrants', 'addr_lookup_complete')
    # ### end Alembic commands ###
