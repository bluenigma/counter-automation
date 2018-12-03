"""Script used for testing. Populates database unit and client tables with mock
data. This module takes a csv file as an argument.
==============================================================================
CSV column structure:

    id | name | black_rate | color_rate | min_monthly_pay

First row is skipped."""

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from modules.db_init import Unit, Counter, Client, Base
from datetime import datetime, date
from random import choice
from sys import argv
import csv

script, csvfile = argv
engine = create_engine('sqlite:///modules/counter_autom.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

###############################################################################
# Populate db with mock clients from csv file

def populate_clients():
    with open(csvfile, 'r') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            new_client = Client(
                id=row[0],
                name=row[1],
                black_rate=row[2],
                color_rate=row[3],
                min_monthly_pay=row[4]
                )
            session.add(new_client)
            session.commit()

###############################################################################
# Populate db with random copiers.

limiter_low = datetime(2018,6,1).date()
limiter_high = datetime(2018,7,1).date()
vendor_list = ['Konica Minolta','Develop']
model_list = ['C203','C220','C280','C360','C666']


def add_unit(sn,black,color):
    """Add a mock unit within specified parameters"""
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

def omit_duplicate_sn(dbquery):
    """Check query for duplicate serial numbers and omit them."""
    a = []
    for obj in dbquery:
        a.append(obj.sn)
    b = list(set(a))
    print("Omitted {} redundant entries.".format(len(dbquery)-len(b)))
    return(b)

def populate_units():
    """Core function of this script."""
    qry = session.query(Counter).filter(and_(Counter.date>=limiter_low,
        Counter.date<limiter_high)).all()
    clean_feed = omit_duplicate_sn(qry)
    ll = []
    for obj in clean_feed:
        qry2 = session.query(Counter).filter(Counter.sn.like(obj)).order_by(
        Counter.id.desc()).first()
        ll.append(qry2)
    for obj in ll:
        add_unit(obj.sn, obj.black_total, obj.color_total)

###############################################################################

if __name__ == '__main__':
    populate_clients()
    client_list = session.query(Client).all()
    populate_units()
