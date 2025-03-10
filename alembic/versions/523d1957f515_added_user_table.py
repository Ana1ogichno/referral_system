"""Added User table

Revision ID: 523d1957f515
Revises: 
Create Date: 2025-02-21 13:37:58.310569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '523d1957f515'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('sid', sa.Uuid(), nullable=False),
    sa.Column('email', sa.String(), nullable=False, comment='email of user'),
    sa.Column('hashed_password', sa.String(), nullable=False, comment='password'),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('sid'),
    sa.UniqueConstraint('sid'),
    schema='users',
    comment='users module schema'
    )
    op.create_unique_constraint("unique_users_user_sid", 'user', ['sid'], schema='users')
    op.create_index(op.f('ix_users_user_email'), 'user', ['email'], unique=True, schema='users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_user_email'), table_name='user', schema='users')
    op.drop_constraint("unique_users_user_sid", 'user', schema='users', type_='unique')
    op.drop_table('user', schema='users')
    # ### end Alembic commands ###
