"""Added power_mode

Revision ID: 81f94b4136ee
Revises: b6020d5b13fc
Create Date: 2023-07-28 19:22:18.654152

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "81f94b4136ee"
down_revision = "b6020d5b13fc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('DeviceMeasurement', 'device_id', existing_type=sa.CHAR(length=32),  nullable=False)
    with op.batch_alter_table("DeviceMeasurement") as batch_op:
        batch_op.drop_column("name")
    op.add_column("devices", sa.Column("power_mode", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("devices", "power_mode")
    op.add_column("DeviceMeasurement", sa.Column("name", sa.VARCHAR(), nullable=False))
    # op.alter_column('DeviceMeasurement', 'device_id', existing_type=sa.CHAR(length=32), nullable=True)
    # ### end Alembic commands ###
