import imaplib, email, re, getpass
from datetime import datetime
from db_init import Counter,Base

a = []

def fetch_email():
    with open('config.txt','r') as config:
        for line in config:
            l1 = line.strip().split('=')
            if l1[0] == 'target_server':
                target_server = l1[1]
            elif l1[0] == 'target_email':
                target_email = l1[1]
            else:
                pass
    target_pwd = getpass.getpass(f'Password for {target_email}: ')
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
    bls1 = sdate.split('/')
    bls1.reverse()
    if len(str(bls1[0])) == 2:
        step = '20' + bls1.pop(0)
        bls1.insert(0,step)
    else:
        pass
    final = str(bls1[0] + '-' + bls1[1] + '-' + bls1[2])
    return datetime.strptime(final,'%Y-%m-%d')

def translate_mails(indata):
    b = {}
    listed_data = []
    c = []

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
                print(name)
                b['name'] = name
            elif re.search(r'Serial Number',record):
                sn = record.strip("[Serial Number], ")
                print(sn)
                b['sn'] = sn
            elif re.search(r'Send Date',record):
                send_date = record.strip("[Send Date],").strip()
                date_t = translate_date(send_date)
                print(date_t)
                b['send date'] = date_t
            elif re.search(r'Total Color Counter',record):
                color_total = int(record.strip("[Total Color Counter],"))
                print(color_total)
                b['color_total'] = color_total
            elif re.search(r'Total Black Counter',record):
                black_total = int(record.strip("[Total Black Counter],"))
                print(black_total)
                b['black total'] = black_total
                a.append(Counter(date=date_t,sn=sn,black_total=black_total,
                color_total=color_total))
            else:
                pass


if __name__ == '__main__':
    #fetch_email()
    translate_mails(fetch_email())
