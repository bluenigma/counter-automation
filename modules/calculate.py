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
    dat = date(year,month,1)
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
            # yield i, dat, target.black_total - prev.black_total, target.color_total - prev.color_total
            newRep = MonthlyPrints(
            sn = i.sn,
            month = dat,
            blackPrints = target.black_total - prev.black_total,
            colorPrints = target.color_total - prev.color_total
            )
            session.add(newRep)
            session.commit()
        elif target is None and prev is None:
            print(f'{i.sn} - No counter report for month {prevMonth}/{year} and {month}/{year}')
            continue
        elif prev is None:
            print(f'{i.sn} - No counter report for month {prevMonth}/{year}')
            continue # yield i, target.black_total - i.black_count, target.color_count - i.color_count
        elif target is None:
            print(f'{i.sn} - No counter report for month {month}/{year}')
            continue
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
        return unit, target.black_total - prev.black_total, target.color_total - prev.color_total
    elif target is None and prev is None:
        return f'{i.sn} - No counter report for month {prevMonth}/{year} and {month}/{year}'
    elif prev is None:
        return f'{i.sn} - No counter report for month {prevMonth}/{year}'
        # yield i, target.black_total - i.black_count, target.color_count - i.color_count
    elif target is None:
        return f'{i.sn} - No counter report for month {month}/{year}'
    else:
        return f'{i.sn} - doh'

def intodb(sn,date,bP,cP):
    newRep = MonthlyPrints(
    sn = sn,
    month = date,
    blackPrints = bP,
    colorPrints = cP
    )
    session.add(newRep)
    session.commit()

mockdate = date(2018,5,1)
def clientPayment(clientid, date):
    '''Calculate monthly payment for client'''
    client = session.query(Client).filter(Client.id==clientid).one()
    prints = session.query(MonthlyPrints).join(Unit).join(Client)\
    .filter(Client.id==clientid)\
    .filter(Unit.sn==MonthlyPrints.sn)\
    .filter(MonthlyPrints.month==date)
    btot = 0
    ctot = 0
    for print in prints:
        btot += print.blackPrints
        ctot += print.colorPrints
    amo = btot * client.black_rate + ctot * client.color_rate
    if amo <= client.min_monthly_pay:
        amo = client.min_monthly_pay
    else:
        pass
    newrep = MonthlyPay(month=date,client=client.id,amount=amo)
    session.add(newrep)
    session.commit()

def run_print_reports():
    for i in range(1,13):
        calculate_month(q,2018,i)

def run_payment_reports():
    q = session.query(Client).all()
    for n in q:
        for i in range(1,13):
            dat = date(2018,i,1)
            clientPayment(n.id,dat)
