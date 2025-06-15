"""
Database configuration and connection management.
"""

import os
from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool, QueuePool
from .models import Base
import logging

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration management."""
    
    def __init__(self):
        # Get database URL from environment or use default
        self.database_url = os.environ.get(
            'DATABASE_URL',
            'postgresql://user:password@localhost:5432/ai_platform'
        )
        
        # Support for different database URLs in different environments
        if os.environ.get('ENV') == 'test':
            self.database_url = os.environ.get(
                'TEST_DATABASE_URL',
                'postgresql://user:password@localhost:5432/ai_platform_test'
            )
        
        # Configure connection pool
        self.pool_size = int(os.environ.get('DB_POOL_SIZE', '10'))
        self.max_overflow = int(os.environ.get('DB_MAX_OVERFLOW', '20'))
        self.pool_timeout = int(os.environ.get('DB_POOL_TIMEOUT', '30'))
        self.pool_recycle = int(os.environ.get('DB_POOL_RECYCLE', '3600'))
        
        # SSL configuration for production
        self.ssl_require = os.environ.get('DB_SSL_REQUIRE', 'false').lower() == 'true'
        
        # Create engine with appropriate settings
        self.engine = self._create_engine()
        
        # Create session factory
        self.SessionLocal = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        )
    
    def _create_engine(self):
        """Create SQLAlchemy engine with appropriate configuration."""
        # Parse database URL and add SSL if required
        connect_args = {}
        if self.ssl_require and 'postgresql' in self.database_url:
            connect_args['sslmode'] = 'require'
        
        # Create engine with connection pooling
        if os.environ.get('ENV') == 'test':
            # Use NullPool for testing to avoid connection issues
            engine = create_engine(
                self.database_url,
                connect_args=connect_args,
                poolclass=NullPool,
                echo=os.environ.get('DB_ECHO', 'false').lower() == 'true'
            )
        else:
            # Use QueuePool for production
            engine = create_engine(
                self.database_url,
                connect_args=connect_args,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_timeout=self.pool_timeout,
                pool_recycle=self.pool_recycle,
                pool_pre_ping=True,  # Verify connections before using
                echo=os.environ.get('DB_ECHO', 'false').lower() == 'true'
            )
        
        # Add event listeners for connection management
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """Enable foreign keys for SQLite."""
            if 'sqlite' in self.database_url:
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        
        return engine
    
    def create_tables(self):
        """Create all database tables."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all database tables. Use with caution!"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Error dropping database tables: {e}")
            raise
    
    @contextmanager
    def get_db_session(self):
        """Context manager for database sessions."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def close(self):
        """Close all database connections."""
        self.SessionLocal.remove()
        self.engine.dispose()


# Global database configuration instance
db_config = DatabaseConfig()


def get_db():
    """Dependency for FastAPI/Flask to get database session."""
    db = db_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database."""
    db_config.create_tables()
    logger.info("Database initialized successfully")


def reset_db():
    """Reset the database (drop and recreate all tables)."""
    db_config.drop_tables()
    db_config.create_tables()
    logger.info("Database reset successfully")