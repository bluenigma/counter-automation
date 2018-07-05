import os
import sys
from sqlalchemy import (Column, ForeignKey, Integer, String, Float,
DateTime, ForeignKey, Sequence)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class Counter(Base):
    __tablename__ = 'counters'
    id = Column(Integer, Sequence('counter_id_seq'), primary_key=True)
    date = Column(String(20))
    sn = Column(String(25), ForeignKey('units.sn'))
    black_total = Column(Integer)
    color_total = Column(Integer)

    counter = relationship('Unit', back_populates='counters')

    def __repr__(self):
        return(
        f'<{self.date}> Counter report <{self.id}> \
        Black {self.black_total}, Color {self.color_total}'
        )

class Unit(Base):
    __tablename__ = 'units'
    id = Column(Integer, Sequence('unit_id_seq'), primary_key=True)
    sn = Column(String(25), unique=True)
    model = Column(String(25))
    city = Column(String(50))
    street = Column(String(50))
    location = Column(String(50))
    black_count = Column(Integer)
    color_count = Column(Integer)
    client_id = Column(Integer, ForeignKey('clients.id'))

    counters = relationship('Counter', back_populates='counter')
    client = relationship('Client', back_populates='units')

    def __repr__(self):
        return(f'Unit {self.sn}\nModel {self.model}')

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, Sequence('client_id_seq'), primary_key=True)
    name = Column(String(50))
    black_rate = Column(Float)
    color_rate = Column(Float)
    min_monthly_pay = Column(Integer)

    units = relationship('Unit', back_populates='client')

    def __repr__(self):
        return(f'<Client: [{self.name}]>')

if __name__ == "__main__":
    engine = create_engine('sqlite:///counter_autom.db')
    Base.metadata.create_all(engine)
