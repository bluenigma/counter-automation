import imaplib, email, re, getpass, configparser
from datetime import datetime, date
from modules.db_init import Counter,Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = configparser.ConfigParser()
config.read('parameters.ini')
target_server = config['DEFAULT']['imap_server']
target_email = config['DEFAULT']['mail_address']

engine = create_engine('sqlite:///modules/counter_autom.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

counterList = []

def fetch_email():
    '''Fetch email from server.'''
    if len(config['DEFAULT']['email_password']) == 0:
        target_pwd = getpass.getpass(f'Password for {target_email}: ')
    else:
        target_pwd = config['DEFAULT']['email_password']
    raw_messages_list = []
    try:
        print(f"Logging in to {target_server}")
        mail = imaplib.IMAP4_SSL(target_server)
        print('OK')
        print(f'Sending credentials for {target_email}')
        mail.login(target_email,target_pwd)
        print('OK')
        mail.select()
        typ, data = mail.search(None, 'ALL')
        for num in data[0].split():
            typ, content = mail.fetch(num, '(RFC822)')
            content_string = str(content[0][1])
            raw_messages_list.append(content_string)
        mail.close()
        mail.logout()
        return raw_messages_list
    except Exception as e:
        print('Something went wrong. ')
        print(f'Error: {e}')

def translate_date(sdate):
    '''Format date string from counter to datetime object.'''
    bls1 = sdate.split('/')
    bls1.reverse()
    if len(str(bls1[0])) == 2:
        step = '20' + bls1.pop(0)
        bls1.insert(0,step)
    else:
        pass
    final = str(bls1[0] + '-' + bls1[1] + '-' + bls1[2])
    return datetime.strptime(final,'%Y-%m-%d').date()

def translate_mails(indata):
    '''Search each mail for counter reports.'''
    listed_data = []
    name = None
    sn = None
    send_date = None
    color_total = None
    black_total = None
    for message in indata:
         listed_data.append(message.split('\\r\\n'))
    for i in range(0,len(listed_data)):
        for record in listed_data[i]:
            if re.search(r'Model Name',record):
                name = record.strip("[Model Name],")
            elif re.search(r'Serial Number',record):
                sn = record.strip("[Serial Number], ")
            elif re.search(r'Send Date',record):
                send_date = record.strip("[Send Date],").strip()
                date_t = translate_date(send_date)
            elif re.search(r'Total Color Counter',record):
                color_total = int(record.strip("[Total Color Counter],"))
            elif re.search(r'Total Black Counter',record):
                black_total = int(record.strip("[Total Black Counter],"))
                counterList.append(Counter(
                date=date_t,
                sn=sn,
                black_total=black_total,
                color_total=color_total
                ))
            else:
                pass


def insert_intable(counter_list):
    '''Insert list of counter objects into db'''
    for element in counter_list:
        session.add(element)
        session.commit()

if __name__ == '__main__':
    translate_mails(fetch_email())
    insert_intable(counterList)
