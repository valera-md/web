from django.db import models
from django.db.models import Model
from django.db.models.functions import Now

from django.contrib.auth.models import User

class Money(Model):
    amount = models.IntegerField(default = 0)
    currency = models.CharField(max_length = 4)
    
class Option(Model):
    # id - automatically added
    name = models.CharField(max_length = 60)
    description = models.CharField(max_length = 1000, default='')
    slug = models.SlugField(max_length=30, unique=True) # like secondary ID
    period = models.IntegerField(default = 1)
    price = models.OneToOneField(Money, on_delete = models.CASCADE)
    #TODO auto generate slugs

class Client (User):
    phone = models.CharField(max_length = 20)

class Bot (User):
    pass

class Message (Model):
    type = models. CharField(max_length = 10) # 'message'. 'reply'
    body = models. CharField(max_length = 20000, null=True) 
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_receiver')
    sent = models.DateTimeField(db_default=Now()) # with tz

class Subscription(Model):
    payed = models.BooleanField(default = False)
    started = models.DateTimeField(null=True) # with tz
    client = models.ForeignKey(
        Client,
        on_delete = models.CASCADE
    )
    option = models.ForeignKey(
        Option,
        on_delete = models.CASCADE
    )
 