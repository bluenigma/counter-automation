import os
import sys
from sqlalchemy import (Column, ForeignKey, Integer, String, Float,
Date, ForeignKey, Sequence, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class Counter(Base):
    __tablename__ = 'counters'
    id = Column(Integer, Sequence('counter_id_seq'), primary_key=True)
    date = Column(Date)
    sn = Column(String(25), ForeignKey('units.sn'))
    black_total = Column(Integer)
    color_total = Column(Integer)

    unit = relationship('Unit', back_populates='counters')

    def __repr__(self):
        return(
        f'<{self.date}> Counter report No. {self.id}'
        f'<Black: {self.black_total}>'
        f'<Color: {self.color_total}>')

class Unit(Base):
    __tablename__ = 'units'
    id = Column(Integer, Sequence('unit_id_seq'), primary_key=True)
    sn = Column(String(25), unique=True)
    vendor = Column(String(50))
    model = Column(String(25))
    black_count = Column(Integer)
    color_count = Column(Integer)
    client_id = Column(Integer, ForeignKey('clients.id'))

    counters = relationship('Counter', back_populates='unit')
    client = relationship('Client', back_populates='units')
    monthlyPrints = relationship('MonthlyPrints', back_populates='unit')

    def __repr__(self):
        return(f'<Unit: {self.sn}, Model: {self.model}>')

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, Sequence('client_id_seq'), primary_key=True)
    name = Column(String(50))
    black_rate = Column(Float)
    color_rate = Column(Float)
    min_monthly_pay = Column(Integer)

    units = relationship('Unit', back_populates='client')
    payments = relationship('MonthlyPay', back_populates='cl_id')

    def __repr__(self):
        return(f'<Client: [{self.name}]>')

class MonthlyPrints(Base):
    __tablename__ = 'monthly prints'
    id = Column(Integer, Sequence('monthlyprints_id_seq'), primary_key=True)
    sn = Column(String(50), ForeignKey('units.sn'))
    month = Column(Date)
    blackPrints = Column(Integer)
    colorPrints = Column(Integer)

    unit = relationship('Unit', back_populates='monthlyPrints')


    def __repr__(self):
        return(f'[{self.month}][{self.sn}][Black: {self.blackPrints}][Color:\
{self.colorPrints}]')

class MonthlyPay(Base):
    __tablename__ = 'monthly income'
    id = Column(Integer, Sequence('monthlypay_id_seq'), primary_key=True)
    month = Column(Date)
    client = Column(String(50), ForeignKey('clients.id'))
    amount = Column(Float)
    paid = Boolean()

    cl_id = relationship('Client',back_populates='payments')


def createDB():
    engine = create_engine('sqlite:///modules/counter_autom.db')
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    engine = create_engine('sqlite:///modules/counter_autom.db')
    Base.metadata.create_all(engine)
