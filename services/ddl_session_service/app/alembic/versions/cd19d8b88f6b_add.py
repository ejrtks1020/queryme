"""add

Revision ID: cd19d8b88f6b
Revises: 7e85bae9f196
Create Date: 2025-07-17 15:40:45.618626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd19d8b88f6b'
down_revision: Union[str, Sequence[str], None] = '7e85bae9f196'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ddl_session', sa.Column('del_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ddl_session', 'del_date')
    # ### end Alembic commands ###
