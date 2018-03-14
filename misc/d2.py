import time
import imaplib
import email

target_server = 'imap.gmail.com'
target_email = "jdfetpy@gmail.com"
target_pwd = 'las12345678'


def fetch_email():
    print(f"Logging in to {target_server}")
    mail = imaplib.IMAP4_SSL(target_server)
    print('OK')
    print(f'Sending credentials for {target_email}')
    mail.login(target_email,target_pwd)
    print('OK')
    mail.select('inbox')

    # http://blog.magiksys.net/parsing-email-using-python-header
    # http://blog.magiksys.net/parsing-email-using-python-content
    
    typ, data = mail.search(None, 'ALL')
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        #typ, data = mail.fetch(num, '(RFC5322)')
        print(data)
        
        print('Message %s\n%s\n' % (num, data[0][1]))

    
    mail.close()
    mail.logout()    
        
if __name__ == '__main__':
    fetch_email()
