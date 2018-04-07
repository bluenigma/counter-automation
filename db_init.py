import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class Counter(Base):
    __tablename__ = 'counter'
    record_id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    sn = Column(String(10))
    black_total = Column(Integer)
    color_total = Column(Integer)

class Unit(Base):
    __tablename__ = 'unit'
    sn = Column(String(10), primary_key=True)
    model = Column(String(15))
    black_count = Column(Integer)
    color_count = Column(Integer)
    client_id = Column(Integer)

class Client(Base):
    __tablename__ = 'client'
    ID = Column(Integer, primary_key=True)
    name = Column(String(35))
    black_rate = Column(Float)
    color_rate = Column(Float)

if __name__ == "__main__":
    engine = create_engine('sqlite:///counter_autom.db')
    Base.metadata.create_all(engine)
