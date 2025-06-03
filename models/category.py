from db import Base
from sqlalchemy import Column, Integer, String


class Category(Base):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)