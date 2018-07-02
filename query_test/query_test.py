from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_init import Counter, Client

engine = create_engine('sqlite:///counter_autom.db')
Session = sessionmaker(bind=engine)
session = Session()

b = [3,20,30]
a = session.query(Client).filter(Client.ID.in_([b[0]])).all()


def querytest():
    que = session.query(Client).filter(Client.name.ilike('%'+input('?>')+'%')).all()
    return que
