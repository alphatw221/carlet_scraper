"""update

Revision ID: 82f7f2c17da4
Revises: bc789f49bf91
Create Date: 2023-10-27 13:47:30.027491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82f7f2c17da4'
down_revision: Union[str, None] = 'bc789f49bf91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car', sa.Column('model_category', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car', 'model_category')
    # ### end Alembic commands ###
