"""empty message

Revision ID: 5865f0ec8b6d
Revises: 3c2d5095e224
Create Date: 2023-03-14 15:11:54.382701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5865f0ec8b6d'
down_revision = '3c2d5095e224'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    # ### end Alembic commands ###