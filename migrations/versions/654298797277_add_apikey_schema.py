"""Upgrade DB Schema

Revision ID: 654298797277
Revises: 31a4ed468b18
Create Date: 2018-12-23 22:18:01.904885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '654298797277'
down_revision = '31a4ed468b18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apikey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.create_table('domain_apikey',
    sa.Column('domain_id', sa.Integer(), nullable=True),
    sa.Column('apikey_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apikey_id'], ['apikey.id'], ),
    sa.ForeignKeyConstraint(['domain_id'], ['domain.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('domain_apikey')
    op.drop_table('apikey')
    # ### end Alembic commands ###
