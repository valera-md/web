print() # /n

import sys
sys.path.append("F:/Python/web/server")

#import psycopg2
from orm.Client import *
from orm.ClientRepository import *
from datetime import datetime

cr = ClientRepository()
clients  = cr.findAll()

file = open("templates/header.html")
header = file.read()
file = open("templates/footer.html")
footer = file.read()
print(header)
print('<h1 style="text-align: center";>MINI SOCIAL / USERS</h1>')
# show users
#print(clients)
for client in clients:
    print(client, "<br/>")
print(footer)
