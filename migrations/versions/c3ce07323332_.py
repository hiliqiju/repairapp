"""empty message

Revision ID: c3ce07323332
Revises: f23a0ac3b555
Create Date: 2020-10-30 13:52:00.654557

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c3ce07323332'
down_revision = 'f23a0ac3b555'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('repair', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.drop_constraint('repair_ibfk_1', 'repair', type_='foreignkey')
    op.create_foreign_key(None, 'repair', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'repair', type_='foreignkey')
    op.create_foreign_key('repair_ibfk_1', 'repair', 'users', ['user_id'], ['id'])
    op.alter_column('repair', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    # ### end Alembic commands ###
