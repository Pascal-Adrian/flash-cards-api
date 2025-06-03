from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Card(Base):
    __tablename__ = 'Cards'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(200), nullable=False)
    answer = Column(String(255), nullable=False)
    set_id = Column(Integer, ForeignKey('Sets.id'), nullable=False)
    set = relationship("Set", back_populates="cards")
