"""empty message

Revision ID: 35fc29f53f54
Revises: 102533aa4cc0
Create Date: 2022-08-02 19:22:55.357638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35fc29f53f54'
down_revision = '102533aa4cc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('icon', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'icon')
    # ### end Alembic commands ###
