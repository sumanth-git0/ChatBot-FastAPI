from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os

# -----------------------------
# 1️⃣ Load .env explicitly
# -----------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set. Make sure .env has DATABASE_URL pointing to Docker Postgres.")

print("ALEMBIC USING DATABASE:", DATABASE_URL)  # debug check

# -----------------------------
# 2️⃣ Import models & metadata
# -----------------------------
from app.models import *
from app.database import Base

target_metadata = Base.metadata

# -----------------------------
# 3️⃣ Alembic config object
# -----------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -----------------------------
# 4️⃣ Helper to get DB URL
# -----------------------------
def get_database_uri():
    return DATABASE_URL

# -----------------------------
# 5️⃣ Offline migrations
# -----------------------------
def run_migrations_offline() -> None:
    url = get_database_uri()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# -----------------------------
# 6️⃣ Online migrations
# -----------------------------
def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    assert configuration
    configuration["sqlalchemy.url"] = get_database_uri()

    connectable = engine_from_config(
        configuration=configuration,
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

# -----------------------------
# 7️⃣ Execute
# -----------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
