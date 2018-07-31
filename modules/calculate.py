from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.db_init import *

engine = create_engine('sqlite:///modules/counter_autom.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


qry = session.query(Counter, Unit).filter(Unit.sn==Counter.sn).order_by(Unit.sn)
