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
                                        Counter.date<limiter_high)).all()
def remove_duplicate_sn(dbquery):
    a = []
    for obj in dbquery:
        a.append(obj.sn)
    b = list(set(a))
    print("Removed {} redundant entries.".format(len(dbquery)-len(b)))
    return(b)


clean_feed = remove_duplicate_sn(qry)
ll = []
for obj in clean_feed:
    qry2 = session.query(Counter).filter(Counter.sn.like(obj)).order_by(
        Counter.id.desc()).first()
    ll.append(qry2)

# for obj in ll:
#     print(obj)
# print('-'*10)
# print(len(ll))

for obj in ll:
    populate(obj.sn, obj.black_total, obj.color_total)
