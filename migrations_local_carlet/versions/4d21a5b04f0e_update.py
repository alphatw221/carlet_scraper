"""update

Revision ID: 4d21a5b04f0e
Revises: 
Create Date: 2023-12-07 14:43:54.927051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4d21a5b04f0e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicle_model', sa.Column('auto_data_id', mysql.BIGINT(), nullable=True, comment='Auto Data ID'))
    op.add_column('vehicle_model', sa.Column('tire_rack_id', mysql.BIGINT(), nullable=True, comment='Tire Rack ID'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vehicle_model', 'tire_rack_id')
    op.drop_column('vehicle_model', 'auto_data_id')
    # ### end Alembic commands ###