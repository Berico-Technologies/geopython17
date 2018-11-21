"""empty message

Revision ID: fe71661b0cd7
Revises: 
Create Date: 2017-04-19 11:37:59.869825

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision = 'fe71661b0cd7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    conn = op.get_bind()

    function_create = """
    CREATE FUNCTION exec(text) returns text language plpgsql volatile AS $f$ BEGIN EXECUTE $1; RETURN $1; END; $f$;
    """
    function_executor = """
    SELECT exec('ALTER TABLE ' || quote_ident(s.nspname) || '.' || quote_ident(s.relname) || ' OWNER TO rds_superuser;')
      FROM (
        SELECT nspname, relname
        FROM pg_class c JOIN pg_namespace n ON (c.relnamespace = n.oid)
        WHERE nspname in ('tiger','topology') AND
        relkind IN ('r','S','v') ORDER BY relkind = 'S')
    s;
    """

    conn.execute("CREATE EXTENSION postgis;")
    conn.execute("CREATE EXTENSION fuzzystrmatch;")
    conn.execute("CREATE EXTENSION postgis_tiger_geocoder;")
    conn.execute("CREATE EXTENSION postgis_topology;")
    conn.execute("ALTER SCHEMA tiger OWNER TO rds_superuser;")
    conn.execute("ALTER SCHEMA tiger_data OWNER TO rds_superuser;")
    conn.execute("ALTER SCHEMA topology OWNER TO rds_superuser;")
    conn.execute(function_create)
    conn.execute(function_executor)

    op.create_table(
        'mapping',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='LINESTRING', srid=4326), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mapping')
    # ### end Alembic commands ###
