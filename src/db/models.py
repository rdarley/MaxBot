from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import relationship

Base = declarative_base()


class Inspiration(Base):
    __tablename__ = 'inspiration'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    server = Column(String)
    url = Column(String)
    member_id = Column(Integer, ForeignKey('member.id'))

class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    inspirations = relationship("Inspiration")