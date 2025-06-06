from db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Set(Base):
    __tablename__ = 'Sets'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(String(255), nullable=False)
    level = Column(Integer, nullable=False, default=0)
    last_opened = Column(DateTime, nullable=True)
    category_id = Column(Integer, ForeignKey('Categories.id'), nullable=False)
    category = relationship("Category", back_populates="sets")
    tags = relationship("Tag", secondary="SetTag", back_populates="sets")
    cards = relationship("Card", back_populates="set", cascade="all, delete-orphan")


