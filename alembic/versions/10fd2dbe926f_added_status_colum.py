"""added status colum

Revision ID: 10fd2dbe926f
Revises: 8a0d85144a33
Create Date: 2025-07-12 00:46:03.697621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql



# revision identifiers, used by Alembic.
revision: str = '10fd2dbe926f'
down_revision: Union[str, None] = '8a0d85144a33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


employee_status_enum = postgresql.ENUM(
    'ACTIVE', 'NOT_STARTED', 'TERMINATED',
    name='employee_status_enum'
)

def upgrade():
    # 1. Create the enum type
    employee_status_enum.create(op.get_bind())

    # 2. Add the column using the new type
    op.add_column('employees',
        sa.Column('status', employee_status_enum, nullable=False, server_default='ACTIVE')
    )


def downgrade():
    # 1. Drop the column first
    op.drop_column('employees', 'status')

    # 2. Drop the enum type
    employee_status_enum.drop(op.get_bind())