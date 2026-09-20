from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./support_crm.db"

# connect_args is SQLite-specific: by default SQLite only allows
# one thread to talk to a connection; FastAPI can use multiple
# threads for a single request, so we relax that restriction.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency: gives each request its own DB session, and guarantees
# it's closed afterward even if an error happens.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()