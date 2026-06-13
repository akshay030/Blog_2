from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from src.utils.settings import settings


engine = create_engine(url=settings.DB_CONNECTION)

LocalSession = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()