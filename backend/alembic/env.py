from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Import our app's settings and models so Alembic knows the real DB URL
# and the real table definitions, instead of guessing from alembic.ini.
from app.core.config import settings
from app.db import Base
from app.models.resume import Resume  # noqa: F401 -- import registers the model

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This tells Alembic "here is the full picture of what tables SHOULD
# exist" -- it compares this against the real database when you run
# `alembic revision --autogenerate`.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    # Override whatever was in alembic.ini with our real settings URL --
    # single source of truth stays in app/core/config.py.
    configuration["sqlalchemy.url"] = settings.database_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
