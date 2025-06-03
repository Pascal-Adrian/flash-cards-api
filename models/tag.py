from db import Base
from sqlalchemy import Column, Integer, String


class Tag(Base):
    __tablename__ = 'Tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    color = Column(String(30), nullable=True)