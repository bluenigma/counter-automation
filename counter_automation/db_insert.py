from os import system
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_init import Counter, Base


engine = create_engine('sqlite:///counter_autom.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def insert_intable(obj_list):
    for element in obj_list:
        new_counter = Counter(date=element.date, sn=element.sn, black_total=element.black_total, color_total=element.color_total)
        session.add(new_counter)
        session.commit()
