import configparser, getpass

mail_address = input("Email address that will be searched for counters:\n> ")
imap_server = input("IMAP Server:\n> ")
while True:
    print("""Remember email password? NOTE: If yes, it will be stored in plaintext.""")
    remember_password = input("y/n\n> ").lower()
    if remember_password == "y":
        email_password = getpass.getpass("Enter password for mailbox:\n> ")
        break
    elif remember_password == "n":
        email_password = ''
        break
    else:
        continue
config = configparser.ConfigParser()
config['DEFAULT'] = {'database' : 'counter_autom.db',
                    'mail_address' : mail_address,
                    'imap_server' : imap_server,
                    'email_password' : email_password}

with open('parameters.conf', 'w') as configfile:
    config.write(configfile)

print("Setup complete. You can always re-run this script to change settings.")
