"""initial migration

Revision ID: 666ca1d9187c
Revises: 
Create Date: 2022-05-22 16:12:23.221939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '666ca1d9187c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('favourite_announcements', sa.ARRAY(sa.Integer()), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('announcement',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('announcement_type', sa.Integer(), nullable=False),
    sa.Column('parking_type', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('announced_date', sa.DateTime(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('announcement')
    op.drop_table('user')
    # ### end Alembic commands ###