import imaplib
import email
import re

target_server = 'imap.gmail.com'
target_email = "jdfetpy@gmail.com"
target_pwd = 'las12345678'

raw_messages_list = []
a = []




def fetch_email():
    try:
        print(f"Logging in to {target_server}")
        mail = imaplib.IMAP4_SSL(target_server)
        print('OK')
        print(f'Sending credentials for {target_email}')
        mail.login(target_email,target_pwd)
        print('OK')
        mail.select()
        
        # http://blog.magiksys.net/parsing-email-using-python-header
        # http://blog.magiksys.net/parsing-email-using-python-content
        
        typ, data = mail.search(None, 'ALL')
        
        
        
        for num in data[0].split():
            typ, content = mail.fetch(num, '(RFC822)')
            content_string = str(content[0][1])
            raw_messages_list.append(content_string)

        
        mail.close()
        mail.logout()
    except Exception as e:
        print('Something went wrong. ')
        print(f'Error: {e}')
        

def translate_mails(indata):
    b = {}
    c = []
    
    for message in indata:
        listed_data = message.split('\\r\\n')
        c.append(listed_data)
        
    for message_element in c:
        if re.search(r'Model Name',message_element):
            name = message_element.strip("[Model Name],")
            print(name)
            b['name'] = name
        elif re.search(r'Serial Number',message_element):
            sn = message_element.strip("[Serial Number], ")
            print(sn)
            b['sn'] = sn
        elif re.search(r'Send Date',message_element):
            send_date = message_element.strip("[Send Date],")
            print(send_date)
            b['send date'] = send_date
        elif re.search(r'Total Color Counter',message_element):
            color_total = int(message_element.strip("[Total Color Counter],"))
            print(color_total)
            b['color_total'] = color_total
        elif re.search(r'Total Black Counter',message_element):
            black_total = int(message_element.strip("[Total Black Counter],"))
            print(black_total)
            b['black total'] = black_total
        else:
            pass
    a.append(b)
        
        
if __name__ == '__main__':
    fetch_email()
    translate_mails(raw_messages_list)
