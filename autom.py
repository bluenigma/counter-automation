import imaplib
import email
import re
import getpass
from clm import rd

target_server = 'imap.gmail.com'
target_email = "jdfetpy@gmail.com"
target_pwd = getpass.getpass(f'Password for {target_email}: ')


a = []




def fetch_email():
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
                send_date = record.strip("[Send Date],")
                print(send_date)
                b['send date'] = send_date
            elif re.search(r'Total Color Counter',record):
                color_total = int(record.strip("[Total Color Counter],"))
                print(color_total)
                b['color_total'] = color_total
            elif re.search(r'Total Black Counter',record):
                black_total = int(record.strip("[Total Black Counter],"))
                print(black_total)
                b['black total'] = black_total
                a.append(rd(sn, name, send_date, color_total, black_total))
            else:
                pass
        
        
    
        
        
        
if __name__ == '__main__':
    #fetch_email()
    translate_mails(fetch_email())
