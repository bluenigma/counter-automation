import os
from modules import autom
from modules import db_init
from modules import db_insert
from os.path import exists

def check_db():
    # Check if database exists, if not, create it
    if not exists('modules/counter_autom.db'):
        os.system('python modules/db_init.py')
    else:
        pass

check_db()
autom.translate_mails(autom.fetch_email())
db_insert.insert_intable(autom.a)
