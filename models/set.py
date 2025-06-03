from db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class Set(Base):
    __tablename__ = 'Sets'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    title = Column(String(100), index=True, nullable=False)
    description = Column(String(255), nullable=False)
    level = Column(Integer, nullable=False, default=0)
    last_opened = Column(DateTime, nullable=True)
    category_id = Column(Integer, index=True, nullable=True)
    category = relationship('Category', back_populates='sets', uselist=False)
    cards = relationship('Card', back_populates='set', cascade='all, delete-orphan')
    tags = relationship('Tag', back_populates='sets', secondary='SetTags')
