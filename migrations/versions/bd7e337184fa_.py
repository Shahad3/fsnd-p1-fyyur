"""empty message

Revision ID: bd7e337184fa
Revises: 3f2a7b886402
Create Date: 2020-12-25 11:24:37.054522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd7e337184fa'
down_revision = '3f2a7b886402'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Artist', ['name'])
    op.add_column('Venue', sa.Column('genere', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'Venue', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue', type_='unique')
    op.drop_column('Venue', 'genere')
    op.drop_constraint(None, 'Artist', type_='unique')
    # ### end Alembic commands ###