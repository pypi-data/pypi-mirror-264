"""add_created_by

Revision ID: fa319f214160
Revises: ad4b1b4d1e9d
Create Date: 2022-10-19 09:35:42.371899

"""
import sqlalchemy as sa
from alembic import op

import nebula

# revision identifiers, used by Alembic.
revision = "fa319f214160"
down_revision = "ad4b1b4d1e9d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("deployment", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_by",
                nebula.server.utilities.database.Pydantic(
                    nebula.server.schemas.core.CreatedBy
                ),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "updated_by",
                nebula.server.utilities.database.Pydantic(
                    nebula.server.schemas.core.UpdatedBy
                ),
                nullable=True,
            )
        )

    with op.batch_alter_table("flow_run", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_by",
                nebula.server.utilities.database.Pydantic(
                    nebula.server.schemas.core.CreatedBy
                ),
                nullable=True,
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("flow_run", schema=None) as batch_op:
        batch_op.drop_column("created_by")

    with op.batch_alter_table("deployment", schema=None) as batch_op:
        batch_op.drop_column("updated_by")
        batch_op.drop_column("created_by")

    # ### end Alembic commands ###
