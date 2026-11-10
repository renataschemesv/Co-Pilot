from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Settings
from .models import Base

engine = create_engine(Settings.database_url(), echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
