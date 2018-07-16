import time
from modules.copins import *

print("Imports up to this point completed successfully.")
def test_client_modify_blackrate():
    qry = (session.query(Client).filter(Client.id.like('1')).all())
    startTime = time.time()
    client_modify_blackrate(qry)
    print('The script took {0} seconds'.format(time.time()-startTime))

test_client_modify_blackrate()
print("Body executed without error")
