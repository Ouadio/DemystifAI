"""migration done

Revision ID: cf8242e46f8c
Revises: 
Create Date: 2020-02-11 18:10:23.496186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf8242e46f8c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pseudo', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('password_hash', sa.String(length=150), nullable=True),
    sa.Column('fullname', sa.Text(), nullable=True),
    sa.Column('birthdate', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('pseudo')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###