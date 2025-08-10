# backend/database.py

from sqlalchemy import create_engine
# Make sure this line is present and correct
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The same database URL from our ingestion script
SQLALCHEMY_DATABASE_URL = "postgresql://kinograph_user:kinograph_password@localhost/kinograph_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the critical line that creates the Base class.
# Our database models in models.py will inherit from this class.
Base = declarative_base()

# This dependency will create a new database session for each request
# and close it when it's done.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()