from lib.db import * 
from .Client import *
from .Repository import Repository

# Repository pattern - storage operations 
class ClientRepository(Repository):
#CRUD / BREAD
    #def __init__(self):
        ##self.conn, self.cur = connect()
        #conn = connect()
        #self.conn = conn[0]
        #self.curs = conn[1]
        # HW1: this function should return a list of all Client objects
    def findAll(self):
        self.curs.execute(f"""
            SELECT * FROM clients
            """)
        #print(self.curs.fetchall())
        #data_all = self.curs.fetchall()
        #print(data_all, type(data_all), type(data_all[0]))
        #clients = []
        #for data in data_all:
             #c = Client(*data)(data[0], data[1], data[2], data[3], data[4], data[5])
             #clients.append(c)
        #     clients.append(Client(*data))
        #clients = list(map(lambda data: Client(*data),data_all))
        #return clients
        return list(map(lambda data: Client(*data),self.curs.fetchall()))
    
    def findById(self, id):
        self.curs.execute(f"""
            SELECT * FROM clients
            WHERE
            id = {id};
            """)
        #print(self.curs.fetchone())
        data = self.curs.fetchone()
        return Client(*data)
    def countByEmailOrPhone(self, phone, email):
            self.curs.execute(f"""
            SELECT COUNT(*) FROM clients
            WHERE
            phone = '{phone}'
            OR
            email = '{email}';
            """)
            return self.curs.fetchone()[0]
    def save(self, client):
        self.curs.execute(f"""
            INSERT INTO clients VALUES(
            {client.id},
            '{client.name}',
            '{client.type}',
            '{client.phone}',
            '{client.email}',
            '{client.password}',
            '{client.active}',
            '{client.registered_on}'
                );
            """)
        self.conn.commit()
    def update(self, client):
        self.curs.execute(f"""
            UPDATE clients SET
            name = '{client.name}',
            phone = '{client.phone}',
            email = '{client.email}'
            WHERE id = {client.id};
            """)
        self.conn.commit()
    def delete(self, client):
        self.curs.execute(f"""
            DELETE FROM clients
            WHERE
            id = {client.id};
            """)
        self.conn.commit()

