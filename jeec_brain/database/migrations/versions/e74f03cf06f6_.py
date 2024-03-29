"""empty message

Revision ID: e74f03cf06f6
Revises: 45fb972f08ad
Create Date: 2019-11-11 00:40:56.671716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e74f03cf06f6'
down_revision = '45fb972f08ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auctions', sa.Column('closing_date', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('auctions', 'closing_date')
    # ### end Alembic commands ###
