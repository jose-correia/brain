"""empty message

Revision ID: a952eb26e558
Revises: b897e2ac23fb
Create Date: 2022-03-17 19:42:16.008044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a952eb26e558'
down_revision = 'b897e2ac23fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('code_per_company', sa.Boolean(), nullable=True))
    op.add_column('student_activities', sa.Column('company_id', sa.Integer(), nullable=False))
    op.drop_constraint('uix_student_activities', 'student_activities', type_='unique')
    op.create_unique_constraint('uix_student_activities', 'student_activities', ['student_id', 'activity_id', 'company_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uix_student_activities', 'student_activities', type_='unique')
    op.create_unique_constraint('uix_student_activities', 'student_activities', ['student_id', 'activity_id'])
    op.drop_column('student_activities', 'company_id')
    op.drop_column('activities', 'code_per_company')
    # ### end Alembic commands ###
