from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import logging
from app import db

# Configure logging
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config.set_main_option('sqlalchemy.url', 'sqlite:///instance/montpellier.db')

target_metadata = db.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
