#!/usr/bin/env python3
"""
Standalone Database Setup for Intelligence Gathering Platform
Creates SQLite database and initializes schema for Termux/standalone deployments
"""

import os
import sys
import logging
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_standalone_database():
    """Setup SQLite database for standalone deployment"""
    
    try:
        # Set SQLite database URL
        db_path = backend_dir / "intelligence_platform.db"
        os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
        
        logger.info(f"Setting up SQLite database at: {db_path}")
        
        # Import database components
        from app.db.database import engine, Base
        from app.db import models
        
        # Create all tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Create initial admin user
        from sqlalchemy.orm import sessionmaker
        from app.db.models import User, UserRole
        from passlib.context import CryptContext
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Check if admin user exists
        admin_user = session.query(User).filter(User.email == "admin@platform.local").first()
        
        if not admin_user:
            logger.info("Creating default admin user...")
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            admin_user = User(
                email="admin@platform.local",
                username="admin",
                hashed_password=pwd_context.hash("admin123"),
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True
            )
            session.add(admin_user)
            session.commit()
            
            logger.info("✅ Admin user created:")
            logger.info("   Email: admin@platform.local")
            logger.info("   Password: admin123")
            logger.info("   ⚠️ Change password after first login!")
        
        session.close()
        
        logger.info("✅ Database setup completed successfully")
        logger.info(f"Database location: {db_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    success = setup_standalone_database()
    sys.exit(0 if success else 1)