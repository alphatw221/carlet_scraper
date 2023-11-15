"""update

Revision ID: 9bd23bb4a0d6
Revises: 2edadcb2ffb5
Create Date: 2023-11-07 12:34:11.924470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '9bd23bb4a0d6'
down_revision: Union[str, None] = '2edadcb2ffb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vehicle', 'year')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicle', sa.Column('year', mysql.YEAR(), nullable=False, comment='年份'))
    # ### end Alembic commands ###