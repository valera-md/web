from django.db import models
from django.db.models import Model

from django.contrib.auth.models import User

class Money(Model):
    amount = models.IntegerField(default = 0)
    currency = models.CharField(max_length = 4)
    
class Option(Model):
    # id - automatically added
    name = models.CharField(max_length = 60)
    period = models.IntegerField(default = 1)
    price = models.OneToOneField(Money, on_delete = models.CASCADE)

class Client(User):
    phone = models.CharField(max_length = 20)

class Subscription(Model):
    payed = models.BooleanField(default = False)
    client = models.ForeignKey(
        Client,
        on_delete = models.CASCADE
    )
    option = models.ForeignKey(
        Option,
        on_delete = models.CASCADE
    )
 