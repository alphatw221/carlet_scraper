"""update

Revision ID: 1cca9dc057e6
Revises: bd8ac0bc8304
Create Date: 2023-10-17 16:48:06.471230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cca9dc057e6'
down_revision: Union[str, None] = 'bd8ac0bc8304'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car', sa.Column('make_name', sa.String(length=32), nullable=True))
    op.add_column('car', sa.Column('model_name', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car', 'model_name')
    op.drop_column('car', 'make_name')
    # ### end Alembic commands ###
