"""'initial'

Revision ID: b7a56e7ea079
Revises: 
Create Date: 2023-02-11 22:16:05.420826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7a56e7ea079'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scripts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('date_create', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('vulnerability_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('scans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('date_start', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('date_end', sa.DateTime(timezone=True), nullable=True),
    sa.Column('risk_level', sa.String(length=255), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.Column('result', sa.Text(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('vulnerability_type', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.ForeignKeyConstraint(['vulnerability_type'], ['vulnerability_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scans')
    op.drop_table('vulnerability_types')
    op.drop_table('users')
    op.drop_table('scripts')
    # ### end Alembic commands ###
