"""empty message

Revision ID: 3bfc040ec91a
Revises: 2f07234deb9e
Create Date: 2025-02-05 11:01:13.650271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '3bfc040ec91a'
down_revision: Union[str, None] = '2f07234deb9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('screenshot', sa.Column('code', sa.Text(), nullable=True))
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.drop_column('screenshot', 'code')
    # ### end Alembic commands ###
