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

    # new_unit = Unit(
    # sn = input_data['sn'],
    # model = input_data['model'],
    # black_count = input_data['black_count'],
    # color_count = input_data['color_count'],
    # )
    while True:
        cnfrm = input('Confirm new unit? (y/n)\n')
        if cnfrm == 'y':
            new_unit = Unit(
            sn = input_data['sn'],
            model = input_data['model'],
            black_count = input_data['black_count'],
            color_count = input_data['color_count'],
            )
            session.add(new_unit)
            session.commit()
            print("New unit created")
            break
        elif cnfrm == 'n':
            print('Cancelled.')
            break
        else:
            pass


def select_unit():
    # Make selection a list for modifying multiple units.
    criteria = input("Type in full or partial serial number:\n>")
    qry = session.query(Unit).filter(Unit.sn.ilike('%'+criteria+'%')).all()
    if len(qry) == 0:
        print("No unit matching specified criteria.")
        select_unit()
    elif len(qry) == 1:
        print(f"Selected {qry[0].sn} | {qry[0].model}")
        selection = qry[0]
        return selection
    elif len(qry) > 1:
        for result in qry:
            print(result.sn)
    else:
        raise Exception("Error in unit selection, starting over.")
        select_unit()






def modify_existing_unit():
    pass

def map_unit_to_client():
    pass

if __name__ == '__main__':
    pass
