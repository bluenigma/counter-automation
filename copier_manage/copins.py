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
            print("New unit created.")
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
        print("-"*10)
        print(f"Selected {qry[0].sn} | {qry[0].model}")
        print("-"*10)
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


def clear_unit_selection():
    print("Clearing all units from selection.")
    selection_unit.clear()

# --------------------------Modify units---------------------------

def unit_modify_sn(target):
    # Can't be implemented until database schema is changed. sn is the primary
    # key for the table.
    pass

def unit_modify_model(target):
    print("This function let's you modify copier's model.\n")
    val = input("Enter new model:\n> ")
    for unit in target:
        unit.model = val
        session.commit()

def unit_modify_bk(target):
    print("This function let's you modify copier's black count.\n")
    try:
        val = int(input("Enter new black counter:\n> "))
        for unit in target:
            unit.black_count = val
            session.commit()
    except ValueError:
        print("Enter a valid number. Starting over.")
        unit_modify_bk(target)


def unit_modify_col(target):
    print("This function let's you modify copier's color count.\n")
    try:
        val = int(input("Enter new color counter:\n> "))
        for unit in target:
            unit.color_count = val
            session.commit()
    except ValueError:
        print("Enter a valid number. Starting over.")
        unit_modify_col(target)



def unit_modify_client_id(target):
    print("This function let's you assign copier or copiers to a client.\n")
    cli = select_client()
    if cli == "Cancelled.":
        return
    else:
        pass
    for unit in target:
        unit.client_id = int(cli.ID)
        session.commit()

# --------------------------------------------------------------
def select_client():
    criteria = input("Select a client or hit RETURN:\n> ")
    if len(criteria) == 0:
        return("Cancelled.")
    else:
        pass
    qry = (session.query(Client).filter(Client.name.ilike
        ('%'+criteria+'%')).all())
    if len(qry) == 0:
        print("No client matching specified criteria.")
        select_client()
    elif len(qry) == 1:
        # selection_client.append(qry[0])
        print(f'Selected {qry[0].name}. Client ID: {qry[0].ID}')
        return(qry[0])
    elif len(qry) > 1:
        print("Multiple clients matching:")
        for result in qry:
            print(f'ID: {result.ID} | {result.name}')
        print('Narrow selection to one client.')
        select_client()

def clear_client_selection():
    print("Clearing client selection.")
    selection_client.clear()

# ---------------------------------------------------------------
select_units()
unit_modify_client_id(selection_unit)

# ---------------------------------------------------------------
if __name__ == '__main__':
    pass
