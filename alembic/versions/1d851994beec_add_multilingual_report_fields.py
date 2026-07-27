"""add multilingual report fields

Revision ID: 1d851994beec
Revises:
Create Date: 2026-07-27 23:22:03.505164

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d851994beec'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""


    # ახალი ქართული/ინგლისური ველები
    op.add_column(
        'reports',
        sa.Column(
            'title_ka',
            sa.String(),
            nullable=True
        )
    )


    op.add_column(
        'reports',
        sa.Column(
            'title_en',
            sa.String(),
            nullable=True
        )
    )


    op.add_column(
        'reports',
        sa.Column(
            'description_ka',
            sa.Text(),
            nullable=True
        )
    )


    op.add_column(
        'reports',
        sa.Column(
            'description_en',
            sa.Text(),
            nullable=True
        )
    )


    # ძველი მონაცემების დაკოპირება ახალ ქართულ ველებში
    op.execute("""
        UPDATE reports
        SET
            title_ka = title,
            description_ka = description
        WHERE title_ka IS NULL
    """)



def downgrade() -> None:
    """Downgrade schema."""


    op.drop_column(
        'reports',
        'description_en'
    )


    op.drop_column(
        'reports',
        'description_ka'
    )


    op.drop_column(
        'reports',
        'title_en'
    )


    op.drop_column(
        'reports',
        'title_ka'
    )