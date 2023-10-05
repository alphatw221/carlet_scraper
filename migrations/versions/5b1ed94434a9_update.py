"""update

Revision ID: 5b1ed94434a9
Revises: d9b22dd0ed03
Create Date: 2023-10-05 02:31:15.294406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b1ed94434a9'
down_revision: Union[str, None] = 'd9b22dd0ed03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('differential', 'code',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=255),
               existing_nullable=True)
    op.alter_column('engine', 'code',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=255),
               existing_nullable=True)
    op.alter_column('transmission', 'code',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transmission', 'code',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=32),
               existing_nullable=True)
    op.alter_column('engine', 'code',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=32),
               existing_nullable=True)
    op.alter_column('differential', 'code',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=32),
               existing_nullable=True)
    # ### end Alembic commands ###
