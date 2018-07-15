"""empty message

Revision ID: d84e3212bc7b
Revises: 527e8f16751e
Create Date: 2018-07-15 17:00:31.068117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd84e3212bc7b'
down_revision = '527e8f16751e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('registrants', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('registrants', 'updated_at')
    # ### end Alembic commands ###
