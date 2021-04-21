"""empty message

Revision ID: 602aea728911
Revises: 2ac83ac02109
Create Date: 2021-04-20 18:58:01.694927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '602aea728911'
down_revision = '2ac83ac02109'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_answer_relation',
    sa.Column('answer_id', sa.Integer(), nullable=True),
    sa.Column('test_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['answer_id'], ['answers.id'], ),
    sa.ForeignKeyConstraint(['test_id'], ['tests.id'], )
    )
    op.add_column('tests', sa.Column('finish', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tests', 'finish')
    op.drop_table('test_answer_relation')
    # ### end Alembic commands ###