from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Alembic Config object
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🔧 Add your project root to sys.path so Alembic can find your modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Import the shared Base from your database setup
from app.database import Base

# 📦 Import your models to ensure all tables are registered
from app.models.inventory import Inventory
from app.models.returns import Return
from app.models.ngo_partners import NGOPartner
from app.models.liquidation_partners import LiquidationPartner
from app.models.stores import Store
from app.models.return_remediation import ReturnRemediation
from app.models.remediation_recommendations import RemediationRecommendation


# 🎯 Set target_metadata for Alembic autogenerate
target_metadata = Base.metadata

# 🔁 Migration logic
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
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

# 🚀 Run migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
