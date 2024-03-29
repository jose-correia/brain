"""empty message

Revision ID: 24becb3f405d
Revises: 0211328588b5
Create Date: 2020-01-25 21:25:40.468363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24becb3f405d'
down_revision = '0211328588b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('companies', 'access_cv_platform')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('access_cv_platform', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
