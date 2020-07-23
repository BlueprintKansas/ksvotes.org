"""empty message

Revision ID: 0f2ef5e4ecfd
Revises: 7e02c1d7810c
Create Date: 2020-07-21 18:16:30.967480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f2ef5e4ecfd'
down_revision = '7e02c1d7810c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('registrants', sa.Column('ab_identification_found', sa.Boolean(), nullable=True))
    op.add_column('registrants', sa.Column('identification_found', sa.Boolean(), nullable=True))
    op.add_column('registrants', sa.Column('reg_found', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('registrants', 'reg_found')
    op.drop_column('registrants', 'identification_found')
    op.drop_column('registrants', 'ab_identification_found')
    # ### end Alembic commands ###