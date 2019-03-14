"""Calculate monthly prints for a unit"""

from datetime import datetime,date
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from modules.db_init import *

engine = create_engine('sqlite:///modules/counter_autom.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

monthPrev = 3
monthCurrent = 4
def convertMonth(arg):
    # arg - dec/jan?
    return date(2018,arg,1),date(2018,arg,28)
cMonthL,cMonthH = convertMonth(monthCurrent)
prevMonthL, prevMonthH = convertMonth(monthPrev)

qry = session.query(Counter, Unit).filter(Unit.sn==Counter.sn).order_by(Unit.sn)
q = session.query(Unit).order_by(Unit.sn)

def report(unit,month):
    """Returns Counter object for Unit in month specified by number.

    Args:
        unit - Unit object
        month - month specified by integer

    Returns:
        Counter object
    """
    monthL = date(2018,month,1)
    monthH = date(2018,month,28)
    countObj = session.query(Counter).filter(Counter.sn==unit.sn).filter(and_(
        Counter.date>=monthL,Counter.date<=monthH)).first()
    return countObj

def calculate_month(unitList,month):
    for i in unitList:
        target = report(i,month)
        prev = report(i,month-1)
        if target is None or prev is None:
            continue
        else:
            print("Black: ", target.black_total-prev.black_total, "Color: ",
                target.color_total-prev.color_total)

calculate_month(q,1)
