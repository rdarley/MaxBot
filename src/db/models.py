from sqlalchemy import Column, ForeignKey, String, Integer, engine, create_engine, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.sql import expression, case

Base = declarative_base()

class MaxBotDB():
    def __init__(self, **kwargs):
        self.engine = create_engine('sqlite:///maxbot.db', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_object(self, session, obj):
        try:
            ret = session.query(exists().where(type(obj).id == obj.id))
            if ret:
                session.add(obj)
                session.commit()
        except IntegrityError:
            session.rollback()
            raise Exception
        except DataError:
            session.rollback()
            raise Exception
        except:
            session.rollback()
            raise Exception

    def query_by_filter(self, session, obj_type, *args, sort=None, limit=10):
        filter_value = self.combine_filter(args)
        return session.query(obj_type).filter(filter_value).order_by(sort).limit(limit).all()

    def delete_entry(self, session, obj_type, *args):

        filter_value = self.combine_filter(args)
        entry = session.query(obj_type).filter(filter_value)

        if entry.first() is not None:
            entry.delete()
        else:
            raise Exception

        session.commit()

    def print_database(self, session, obj_type):
        obj_list = session.query(obj_type).all()

        s = ''

        for obj in obj_list:
            s = s + '\n' + obj.id
        return s

    def combine_filter(self, filter_value):
        return expression.and_(filter_value[0])

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
    server = Column(String)
    inspirations = relationship("Inspiration")