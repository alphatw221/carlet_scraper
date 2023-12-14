"""Added account table

Revision ID: 6ddc2504d10e
Revises: fc28759cd94f
Create Date: 2023-09-28 17:20:44.145744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ddc2504d10e'
down_revision: Union[str, None] = 'fc28759cd94f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('engine', 'change_interval',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('engine', 'capacity',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('engine', 'capacity',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=32),
               existing_nullable=False)
    op.alter_column('engine', 'change_interval',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=32),
               existing_nullable=False)
    # ### end Alembic commands ###