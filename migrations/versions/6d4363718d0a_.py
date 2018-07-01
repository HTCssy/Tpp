"""empty message

Revision ID: 6d4363718d0a
Revises: 83377b66d3cd
Create Date: 2018-07-01 13:28:32.720945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d4363718d0a'
down_revision = '83377b66d3cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seat',
    sa.Column('seat_id', sa.Integer(), nullable=False),
    sa.Column('seat_x', sa.Integer(), nullable=True),
    sa.Column('seat_y', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('is_delete', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('cinema_id', sa.Integer(), nullable=True),
    sa.Column('hall_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cinema_id'], ['cinemas.cid'], ),
    sa.ForeignKeyConstraint(['hall_id'], ['hall.hid'], ),
    sa.PrimaryKeyConstraint('seat_id')
    )
    op.create_table('seat_schedule',
    sa.Column('ssid', sa.Integer(), nullable=False),
    sa.Column('seat_id', sa.Integer(), nullable=True),
    sa.Column('cinema_id', sa.Integer(), nullable=True),
    sa.Column('hall_id', sa.Integer(), nullable=True),
    sa.Column('hsid', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('is_delete', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['cinema_id'], ['cinemas.cid'], ),
    sa.ForeignKeyConstraint(['hall_id'], ['hall.hid'], ),
    sa.ForeignKeyConstraint(['hsid'], ['hall_schedule.hsid'], ),
    sa.ForeignKeyConstraint(['seat_id'], ['seat.seat_id'], ),
    sa.PrimaryKeyConstraint('ssid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seat_schedule')
    op.drop_table('seat')
    # ### end Alembic commands ###
