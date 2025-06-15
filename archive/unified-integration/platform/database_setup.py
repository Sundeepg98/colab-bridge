#!/usr/bin/env python3
"""
Database setup and migration script for the AI platform.
"""

import os
import sys
import argparse
import logging
from alembic.config import Config
from alembic import command
from sqlalchemy import text

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ''))

from src.database import db_config, init_db, reset_db
from src.database.models import User
from src.auth import AuthManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_admin_user(email: str, password: str):
    """Create an admin user."""
    with db_config.get_db_session() as db:
        try:
            # Check if admin already exists
            existing_admin = db.query(User).filter(User.email == email).first()
            if existing_admin:
                logger.info(f"Admin user {email} already exists")
                return
            
            # Create admin user
            admin = User(
                email=email,
                password_hash=AuthManager.hash_password(password),
                is_active=True,
                is_verified=True
            )
            
            db.add(admin)
            db.commit()
            logger.info(f"Admin user {email} created successfully")
            
        except Exception as e:
            logger.error(f"Error creating admin user: {e}")
            raise


def init_alembic():
    """Initialize Alembic for database migrations."""
    try:
        # Create alembic directory if it doesn't exist
        alembic_dir = os.path.join(os.path.dirname(__file__), 'alembic')
        if not os.path.exists(alembic_dir):
            os.makedirs(alembic_dir)
            logger.info("Created alembic directory")
        
        # Create alembic.ini if it doesn't exist
        alembic_ini = os.path.join(os.path.dirname(__file__), 'alembic.ini')
        if not os.path.exists(alembic_ini):
            with open(alembic_ini, 'w') as f:
                f.write("""[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = ${DATABASE_URL}

[post_write_hooks]
hooks = black
black.type = console_scripts
black.entrypoint = black
black.options = -l 88

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""")
            logger.info("Created alembic.ini")
        
        # Create alembic env.py
        env_py = os.path.join(alembic_dir, 'env.py')
        if not os.path.exists(env_py):
            with open(env_py, 'w') as f:
                f.write("""from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src.database.models import Base

config = context.config

# Set the database URL from environment variable
config.set_main_option('sqlalchemy.url', os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/ai_platform'))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

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
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
""")
            logger.info("Created alembic env.py")
        
        # Create versions directory
        versions_dir = os.path.join(alembic_dir, 'versions')
        if not os.path.exists(versions_dir):
            os.makedirs(versions_dir)
            logger.info("Created alembic versions directory")
        
        logger.info("Alembic initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing Alembic: {e}")
        raise


def check_database_connection():
    """Check if the database connection is working."""
    try:
        with db_config.get_db_session() as db:
            result = db.execute(text("SELECT 1"))
            result.fetchone()
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description='Database setup for AI platform')
    parser.add_argument('--reset', action='store_true', help='Reset the database (drop all tables)')
    parser.add_argument('--create-admin', action='store_true', help='Create an admin user')
    parser.add_argument('--admin-email', type=str, help='Admin email address')
    parser.add_argument('--admin-password', type=str, help='Admin password')
    parser.add_argument('--init-alembic', action='store_true', help='Initialize Alembic for migrations')
    parser.add_argument('--check-connection', action='store_true', help='Check database connection')
    
    args = parser.parse_args()
    
    # Check connection if requested
    if args.check_connection:
        if check_database_connection():
            print("Database connection successful!")
        else:
            print("Database connection failed!")
            sys.exit(1)
        return
    
    # Initialize Alembic if requested
    if args.init_alembic:
        init_alembic()
        return
    
    # Reset database if requested
    if args.reset:
        response = input("Are you sure you want to reset the database? This will delete all data! (yes/no): ")
        if response.lower() == 'yes':
            logger.info("Resetting database...")
            reset_db()
            logger.info("Database reset complete")
        else:
            logger.info("Database reset cancelled")
            return
    else:
        # Initialize database
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialization complete")
    
    # Create admin user if requested
    if args.create_admin:
        if not args.admin_email or not args.admin_password:
            logger.error("Admin email and password are required")
            parser.error("--admin-email and --admin-password are required when using --create-admin")
        
        create_admin_user(args.admin_email, args.admin_password)
    
    logger.info("Database setup complete!")


if __name__ == "__main__":
    main()