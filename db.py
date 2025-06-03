from functools import lru_cache
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import config

@lru_cache()
def get_settings():
    return config.Settings()


setting = get_settings()

engine = create_engine(f'postgresql+psycopg2://{setting.pg_user}:{setting.pg_password}'
                       f'@{setting.pg_host}:{setting.pg_port}/{setting.pg_database}')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    metadata = MetaData()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()