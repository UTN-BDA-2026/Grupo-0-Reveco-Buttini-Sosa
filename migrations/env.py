import os
from logging.config import fileConfig
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.database.database import Base
from app.models.user import User
from app.models.role import Role
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.staff import Staff

load_dotenv()

# Configuración de Alembic
config = context.config

# Configura el logger
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Se apunta al metadata de los modelos para que Alembic los conozca
target_metadata = Base.metadata

# Se inyecta la URL de la base de datos desde las variables de entorno
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()