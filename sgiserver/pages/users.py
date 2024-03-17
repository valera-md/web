print() # /n

import sys
sys.path.append("F:/Maxtor/Valera/Python/web/server")

#import psycopg2
from orm.Client import *
from orm.ClientRepository import *
from datetime import datetime

'''def connect():
 conn = psycopg2.connect("dbname=chat_db user=postgres password=1234")
 #conn = psycopg2.connect("dbname=chat_db user=postgres password=qazwsx host=localhost port=5889")
 curs = conn.cursor()
 return conn, curs

class Repository:
    def __init__(self):
        conn = connect()
        self.conn = conn[0]
        self.curs = conn[1]

class Client:
    def __init__(self, id, name, type, phone=None, email=None, password=None, active=True, registered_on=datetime.now()):
        self.id = id
        self.name = name
        self.type = type
        self.phone = phone
        self.email = email
        self.password = password
        self.active = active
        self.registered_on = registered_on

    def __str__(self):
        return f"CLIENT: {self.id} | {self.name} | {self.type} | {self.phone} | {self.email} | {self.password} | {self.active} | {self.registered_on}"
    
    def __repr__(self):
        return self.__str__()

class ClientRepository(Repository):

    def findAll(self):
        self.curs.execute(f"""
            SELECT * FROM clients
            """)
        return list(map(lambda data: Client(*data),self.curs.fetchall()))'''

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
