"""update

Revision ID: d9b22dd0ed03
Revises: 8591428dcdc9
Create Date: 2023-10-05 02:07:51.777183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9b22dd0ed03'
down_revision: Union[str, None] = '8591428dcdc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('differential',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=True),
    sa.Column('change_interval', sa.String(length=255), nullable=True),
    sa.Column('capacity', sa.String(length=255), nullable=True),
    sa.Column('viscosity', sa.String(length=255), nullable=True),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('car', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('car', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('cooling_system', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('cooling_system', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('engine', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('engine', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('hydraulic_brake', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('hydraulic_brake', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('power_steering', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('power_steering', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('transmission', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('transmission', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transmission', 'updated_at')
    op.drop_column('transmission', 'created_at')
    op.drop_column('power_steering', 'updated_at')
    op.drop_column('power_steering', 'created_at')
    op.drop_column('hydraulic_brake', 'updated_at')
    op.drop_column('hydraulic_brake', 'created_at')
    op.drop_column('engine', 'updated_at')
    op.drop_column('engine', 'created_at')
    op.drop_column('cooling_system', 'updated_at')
    op.drop_column('cooling_system', 'created_at')
    op.drop_column('car', 'updated_at')
    op.drop_column('car', 'created_at')
    op.drop_table('differential')
    # ### end Alembic commands ###
