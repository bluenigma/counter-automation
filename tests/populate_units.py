from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from modules.db_init import Unit, Counter, Client
from datetime import datetime, date
from random import choice

engine = create_engine('sqlite:///modules/counter_autom.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

limiter_low = datetime(2018,6,1).date()
limiter_high = datetime(2018,7,1).date()
vendor_list = ['Konica Minolta','Develop']
model_list = ['C203','C220','C280','C360','C666']
client_list = session.query(Client).all()

def populate(sn,black,color):
    global vendor_list, model_list, client_list
    vendor = choice(vendor_list)
    model = choice(model_list)
    client_id = choice(client_list).id
    new_unit = Unit(
    sn=sn,
    vendor=vendor,
    model=model,
    black_count=black,
    color_count=color,
    client_id=client_id)
    session.add(new_unit)
    session.commit()

qry = session.query(Counter).filter(and_(Counter.date>=limiter_low,
                                        Counter.date<limiter_high))

for obj in qry:
    print(obj,"//////", obj.sn)

# reports #205 and #208 contain identical serial number, UNIQUE error


for obj in qry:
    populate(obj.sn, obj.black_total, obj.color_total)
