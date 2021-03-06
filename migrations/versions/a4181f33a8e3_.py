"""empty message

Revision ID: a4181f33a8e3
Revises: 
Create Date: 2018-05-23 13:27:53.833577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4181f33a8e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clerks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('county', sa.String(), nullable=True),
    sa.Column('officer', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('fax', sa.String(), nullable=True),
    sa.Column('address1', sa.String(), nullable=True),
    sa.Column('address2', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('zip', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('registrants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_completed_step', sa.Integer(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('is_citizen', sa.Boolean(), nullable=True),
    sa.Column('is_eighteen', sa.Boolean(), nullable=True),
    sa.Column('registration', sa.String(), nullable=True),
    sa.Column('party', sa.String(), nullable=True),
    sa.Column('county', sa.String(), nullable=True),
    sa.Column('lang', sa.String(), nullable=True),
    sa.Column('signed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('registrants')
    op.drop_table('clerks')
    # ### end Alembic commands ###
