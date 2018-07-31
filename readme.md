Overview
=====================
Searches mail inbox for automatic counter notifications from Konica Minolta copiers. Intent of this project is to create a copier/printer rental management
system.

Upon reaching mail inbox, notifications are formatted like this:
```
[Model Name],Sample_name_set_in_copier
[Serial Number], XXXXXXXXXXXX
[Send Date],dd/mm/yy
[Total Counter],00077756
[Total Color Counter],00051822
[Total Black Counter],00025934
```

Installation
--------------------
Install required packages  
`pip install -r requirements.txt`

`python -m modules.setup`  
Insert imap email address, imap server and optionally save password. Note that if password is saved, it will be stored in plaintext. To change email configuration, re-run setup script or edit parameters.conf file.

To search inbox for counter notifications and save them in database:  
`python -m modules.start`

Using `python -m tests.populate_units`, serial numbers from notifications will
be mixed with random data to provide sample records.

In similar manner, `python -m tests.populate_clients` will feed db with sample
clients based on csv file.
