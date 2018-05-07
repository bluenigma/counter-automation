from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_init import Unit, Client, Base

engine = create_engine('sqlite:///counter_autom.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_raw_unit():
    input_data = {
    'sn':input('Enter serial number: '),
    'model':input('Enter model: '),
    'black_count':None,
    'color_count':None,
    'client_id':None,
    }

    new_unit = Unit(
    sn = input_data['sn'],
    model = input_data['model'],
    black_count = input_data['black_count'],
    color_count = input_data['color_count'],
    
    )


def modify_existing_unit():
    pass

def map_unit_to_client():
    pass

if __name__ == '__main__':
