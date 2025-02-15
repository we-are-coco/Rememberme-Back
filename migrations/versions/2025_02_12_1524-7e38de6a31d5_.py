"""empty message

Revision ID: 7e38de6a31d5
Revises: 91208ae374c3
Create Date: 2025-02-12 15:24:41.475981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e38de6a31d5'
down_revision: Union[str, None] = '91208ae374c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('screenshot', sa.Column('brand', sa.String(length=255), nullable=True))
    op.add_column('screenshot', sa.Column('type', sa.String(length=255), nullable=True))
    op.add_column('screenshot', sa.Column('date', sa.String(length=255), nullable=True))
    op.add_column('screenshot', sa.Column('time', sa.String(length=255), nullable=True))
    op.add_column('screenshot', sa.Column('from_location', sa.String(length=255), nullable=True))
    op.add_column('screenshot', sa.Column('to_location', sa.String(length=255), nullable=True))
    op.add_column('screenshot', sa.Column('location', sa.String(length=255), nullable=True))
    op.add_column('screenshot', sa.Column('details', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('screenshot', 'details')
    op.drop_column('screenshot', 'location')
    op.drop_column('screenshot', 'to_location')
    op.drop_column('screenshot', 'from_location')
    op.drop_column('screenshot', 'time')
    op.drop_column('screenshot', 'date')
    op.drop_column('screenshot', 'type')
    op.drop_column('screenshot', 'brand')
    # ### end Alembic commands ###
