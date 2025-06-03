from db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class SetTag(Base):
    __tablename__ = 'SetTag'

    set_id = Column(Integer, ForeignKey('Sets.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('Tags.id'), primary_key=True)

    set = relationship("Set", back_populates="tags")
    tag = relationship("Tag", back_populates="sets")
