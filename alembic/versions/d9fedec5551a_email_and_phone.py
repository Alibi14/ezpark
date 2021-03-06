"""email and phone

Revision ID: d9fedec5551a
Revises: f1c0a70d1218
Create Date: 2022-06-15 23:47:33.520268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9fedec5551a'
down_revision = 'f1c0a70d1218'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(), nullable=True))
    op.add_column('user', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone_number')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
