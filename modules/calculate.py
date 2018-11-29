"""Calculate monthly prints for a unit"""

from datetime import datetime,date
from calendar import monthrange
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from modules.db_init import *

engine = create_engine('sqlite:///modules/counter_autom.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


qry = session.query(Counter, Unit).filter(Unit.sn==Counter.sn).order_by(Unit.sn)
q = session.query(Unit).order_by(Unit.sn)

def getCounter(unit, year, month):
    """Returns Counter object for Unit in month specified by number.

    Args:
        unit - Unit object
        year = year integer
        month - month specified by integer

    Returns:
        countObj - Counter object"""
    dayOne, dayLast = monthrange(year,month)
    monthL = date(year, month,1)
    monthH = date(year, month, dayLast)
    countObj = session.query(Counter).filter(Counter.sn==unit.sn).filter(and_(
        Counter.date>=monthL,Counter.date<=monthH)).first()
    return countObj

# much faster than Single function
def calculate_month(unitList, year, month):
    """Calculate monthly prints.

    Args:
        month - month specified by integer
        unit - List of Unit objects or single Unit object

    Yields:
        Tuple (Unit object, black count, color count)"""
    if month in range(2,13):
        prevMonth = month - 1
    elif month == 1:
        prevMonth = 12
    else:
        raise ValueError("Month outside of 1-12 range")
    for i in unitList:
        target = getCounter(i, year, month)
        prev = getCounter(i, year, prevMonth)
        if target is not None and prev is not None:
            yield i, target.black_total - prev.black_total, target.color_total - prev.color_total
        elif prev is None:
            print(f'{i.sn} - oh')
            continue # yield i, target.black_total - i.black_count, target.color_count - i.color_count
        else:
            print(f'{i.sn} - doh')
            continue

def calculate_monthSingle(unit, year, month):
    if month in range(2,13):
        prevMonth = month - 1
    elif month == 1:
        prevMonth = 12
    else:
        raise ValueError("Month outside of 1-12 range")
    target = getCounter(unit, year, month)
    prev = getCounter(unit, year, prevMonth)
    if target is not None and prev is not None:
        return i, target.black_total - prev.black_total, target.color_total - prev.color_total
    elif prev is None:
        return f'{i.sn} - oh'
        # yield i, target.black_total - i.black_count, target.color_count - i.color_count
    else:
        return f'{i.sn} - doh'



def clientPayment():
    '''Calculate monthly payment for client'''
    pass

import time

bef = time.time()
calculate_month(q,2018,10)
aft = time.time()
t1 = aft - bef
print(t1, ' seconds.')

bef = time.time()
for i in q:
    calculate_monthSingle(i,2018,10)
aft = time.time()
t2 = aft - bef
print(t2, ' seconds.')
