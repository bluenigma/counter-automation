'''
Populates clients table using data from csv file. Intention of this
simple module is to quickly fill database with some dummy data for testing.
This module takes path to a csv file as an argument.
==============================================================================
Column structure:

    id | name | black_rate | color_rate | min_monthly_pay

First row is skipped.
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.db_init import Client, Base
from sys import argv
import csv

engine = create_engine('sqlite:///modules/counter_autom.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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

if __name__ == '__main__':
    script, csvfile = argv
    populate_clients()
