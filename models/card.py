from db import Base
from sqlalchemy import Column, Integer, String


class Card(Base):
    __tablename__ = 'Cards'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(200), nullable=False)
    answer = Column(String(255), nullable=False)
