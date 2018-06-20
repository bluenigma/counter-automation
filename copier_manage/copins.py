from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_init import Unit, Client, Base

engine = create_engine('sqlite:///counter_autom.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

selection_unit = []
selection_client = []

def add_unit():
    input_data = {
    'sn':input('Enter serial number: '),
    'model':input('Enter model: '),
    'black_count':input('Black counter: '),
    'color_count':input('Color counter: '
    ),
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


def select_units():
    global selection
    criteria = input("Type in full or partial serial number."
    " To exit, hit RETURN.\n> ")
    if len(criteria) == 0:
        return
    else:
        pass
    qry = session.query(Unit).filter(Unit.sn.ilike('%'+criteria+'%')).all()
    if len(qry) == 0:
        print("No unit matching specified criteria.")
        select_units()
    elif len(qry) == 1:
        print(f"Selected {qry[0].sn} | {qry[0].model}")
        selection_unit.append(qry[0])
        select_units()
    elif len(qry) > 1:
        print("Multiple units matching:")
        for result in qry:
            print(result.sn + " | " + result.model)
        select_units()
    else:
        raise Exception("Error in unit selection, starting over.")
        select_units()

def clear_selection():
    print("Clearing all units from selection.")
    selection.clear()



def modify_unit():
    pass

def select_client():
    criteria = input("YO!Search client or hit RETURN:\n> ")
    if len(criteria) == 0:
        return
    else:
        pass
    qry = (session.query(Client).filter(Client.name.ilike
        ('%'+criteria+'%')).all())
    if len(qry) == 0:
        print("No client matching specified criteria.")
        select_client()
    elif len(qry) == 1:
        selection_client.append(qry[0])
        print(f'Selected {qry[0].name}. Client ID: {qry[0].ID}')
    elif len(qry) > 1:
        print("Multiple units matching:")
        for result in qry:
            print(f'ID: {result.ID} | {result.name}')
        print('Narrow selection to one client.')
        select_client()



if __name__ == '__main__':
    pass
