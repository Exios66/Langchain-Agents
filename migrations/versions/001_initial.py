"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-02-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create workflow_states table
    op.create_table(
        'workflow_states',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('input_data', sa.Text(), nullable=False),
        sa.Column('state_data', sqlite.JSON(), nullable=False),
        sa.Column('messages', sqlite.JSON(), nullable=False),
        sa.Column('workflow_type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_states_id'), 'workflow_states', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_workflow_states_id'), table_name='workflow_states')
    op.drop_table('workflow_states') 