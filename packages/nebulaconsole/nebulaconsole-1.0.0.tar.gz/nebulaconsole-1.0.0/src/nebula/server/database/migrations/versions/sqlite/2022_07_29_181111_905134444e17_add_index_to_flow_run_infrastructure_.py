"""add-index-to-flow-run-infrastructure_document_id

Revision ID: 905134444e17
Revises: 88c2112b668f
Create Date: 2022-07-29 18:11:11.645359

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "905134444e17"
down_revision = "88c2112b668f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("flow_run", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_flow_run__infrastructure_document_id"),
            ["infrastructure_document_id"],
            unique=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("flow_run", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_flow_run__infrastructure_document_id"))

    # ### end Alembic commands ###
