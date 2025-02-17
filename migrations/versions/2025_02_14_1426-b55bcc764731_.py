"""empty message

Revision ID: b55bcc764731
Revises: bb4739f8db24
Create Date: 2025-02-14 14:26:38.014488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b55bcc764731'
down_revision: Union[str, None] = 'bb4739f8db24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('fcm_token', sa.String(length=4096), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'fcm_token')
    # ### end Alembic commands ###
