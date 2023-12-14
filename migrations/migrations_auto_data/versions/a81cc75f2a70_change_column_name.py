"""change column name

Revision ID: a81cc75f2a70
Revises: 053dd722477c
Create Date: 2023-11-19 00:39:22.936650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a81cc75f2a70'
down_revision: Union[str, None] = '053dd722477c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.alter_column("car", "start_of_perduction_year", new_column_name='start_of_production_year')
    op.alter_column("car", "end_of_perduction_year", new_column_name='end_of_production_year')


def downgrade() -> None:
    pass
