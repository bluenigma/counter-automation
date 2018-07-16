from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.db_init import Unit, Client, Base

engine = create_engine('sqlite:///modules/counter_autom.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

selection_unit = []
selection_client = []

class UniqueError(Exception):
    '''Unit with given serial number already exists in database.'''
# -----------------------------Selector class-----------------------------------
class Selector(object):
    '''Selector for units and clients. Intended to replace select functions'''
    def __init__(self,table,column,criteria):
        self.table = table
        self.column = column
        self.criteria = criteria

    def Fetch(self):
        qry = session.query(self.table).filter(self.column.ilike('%'+self.criteria+'%')).all()
        self.qry = qry
        return qry
        # AttributeError: type object 'Selector' has no attribute 'table'

    def __repr__(self):
        pass
# ------------------------------------------------------------------------------
def add_unit():
    input_data = {
    'sn':input('Enter serial number: '),
    'vendor':input('Enter vendor: '),
    'model':input('Enter model: '),
    'black_count':input('Black counter: '),
    'color_count':input('Color counter: '),
    'client_id':None
    }
    qry = session.query(Unit).filter(Unit.sn.ilike(input_data['sn'])).first()
    if qry != None:
        raise UniqueError(f"Serial number {input_data['sn']} already exists.")

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

def remove_unit(selection):
    for unit in selection:
        prompt = input(f"Permanently remove {unit.sn} | {unit.model} ?")
        if prompt == None:
            session.delete(unit)
        else:
            continue

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

def unit_modify_sn(selection):
    for unit in selection:
        newsn = input("Insert new serial number:\n> ")
        qry = session.query(Unit).filter(Unit.sn.ilike(newsn)).all()
        if len(qry) == 0:
            unit.sn = newsn
            session.commit()
        else:
            print("New serial number conflicting with existing unit:")
            for result in qry:
                print(f'{result.sn} || {result.model} || {result.black_count}\
                || {result.color_count}')
            print('Skipping this unit.')
            continue
    pass

def unit_modify_vendor(selection):
    '''This function let's you modify copier's vendor.'''
    val = input("Enter new vendor:\n> ")
    for unit in selection:
        unit.vendor = val
        session.commit()

def unit_modify_model(selection):
    '''This function let's you modify copier's model.'''
    val = input("Enter new model:\n> ")
    for unit in selection:
        unit.model = val
        session.commit()

def unit_modify_bk(selection):
    '''This function let's you modify copier's black count.'''
    try:
        val = int(input("Enter new black counter:\n> "))
        for unit in selection:
            unit.black_count = val
            session.commit()
    except ValueError:
        print("Enter a valid number. Starting over.")
        unit_modify_bk(selection)

def unit_modify_col(selection):
    '''This function let's you modify copier's color count.'''
    try:
        val = int(input("Enter new color counter:\n> "))
        for unit in selection:
            unit.color_count = val
            session.commit()
    except ValueError:
        print("Enter a valid number. Starting over.")
        unit_modify_col(selection)

def unit_modify_client_id(selection):
    '''This function let's you assign copier or copiers to a client.'''
    cli = select_client()
    if cli == "Cancelled.":
        return
    else:
        pass
    for unit in selection:
        unit.client_id = int(cli.id)
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
        selection_client.append(qry[0])
        return(qry[0])
    elif len(qry) > 1:
        print("Multiple clients matching:")
        for result in qry:
            print(f'ID: {result.id} | {result.name}')
        print('Narrow selection to one client.')
        select_client()

def clear_client_selection():
    print("Clearing client selection.")
    selection_client.clear()

def add_client(name,black_rate,color_rate,min_monthly_pay):
    '''Add new client'''
    # ensure floats at black_rate and color_rate
    new_client = Client(
    name = name,
    black_rate = black_rate,
    color_rate = color_rate,
    min_monthly_pay = min_monthly_pay
    )
    session.add(new_client)
    session.commit()

def client_modify_name(selection):
    # This function should accept only single argument
    pass

def client_modify_blackrate(selection):
    new_rate = input("New rates for black page: ")
    try:
        new_rate = float(new_rate.replace(',','.'))
    except ValueError:
        print("Insert a valid number.")
        return(client_modify_blackrate(selection))
    for client in selection:
        client.black_rate = new_rate
        session.commit()


def client_modify_colorrate(selection):
    new_rate = input("New rates for color page: ")
    try:
        new_rate = float(new_rate.replace(',','.'))
    except ValueError:
        print("Insert a valid number.")
        return(client_modify_colorrate(selection))
    for client in selection:
        client.color_rate = new_rate
        session.commit()

def client_modify_min_monthly(selection):
    new_minmonth = input("New minimal monthly payment: ")
    try:
        new_minmonth = int(new_minmonth)
    except ValueError:
        print("Insert a valid number.")
        return(client_modify_min_monthly(selection))
    for client in selection:
        client.min_monthly_pay = new_minmonth
        session.commit()

# ---------------------------------------------------------------
if __name__ == '__main__':
    pass
