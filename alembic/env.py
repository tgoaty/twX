import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.config import DATABASE_URL

from app.models import Base, User  # noqa: F401

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


config = context.config
fileConfig(config.config_file_name)
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")
DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")

config.set_main_option("sqlalchemy.url", DATABASE_URL)


target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
