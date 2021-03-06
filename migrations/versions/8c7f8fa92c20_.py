"""empty message

Revision ID: 8c7f8fa92c20
Revises: c925e4d07621
Create Date: 2018-08-17 13:09:27.720622

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8c7f8fa92c20'
down_revision = 'c925e4d07621'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('registrants', sa.Column('ab_completed_at', sa.DateTime(), nullable=True))
    op.add_column('registrants', sa.Column('ab_permanent', sa.Boolean(), nullable=True))
    op.add_column('registrants', sa.Column('vr_completed_at', sa.DateTime(), nullable=True))
    op.drop_column('registrants', 'completed_at')
    op.drop_column('registrants', 'last_completed_step')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('registrants', sa.Column('last_completed_step', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('registrants', sa.Column('completed_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('registrants', 'vr_completed_at')
    op.drop_column('registrants', 'ab_permanent')
    op.drop_column('registrants', 'ab_completed_at')
    # ### end Alembic commands ###
