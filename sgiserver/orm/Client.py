#ORM + Domain мы разрабатываем бизнес логику приложения
#DDD - Domain Driven Design, почитать и понять что такое домеин приложение, сущность, сам домен, агрегат и т. д. , 7-8 терминов, рекомендую почитить, базовое понимание этого - это хороший плюс для канидата.
#Entity / Model сущность, класс это сущность
from datetime import datetime

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
