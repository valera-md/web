#from django.http import HttpResponse

#def homePage(request):
#    return HttpResponse("Home Page!")

#def signupPage(request):
#    return HttpResponse("Signup Page!")

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from app.models import Option, Money, Client, Subscription, Message, Bot

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
import os

import requests
import json
import markdown

import stripe
stripe.api_key = "api_key"

def homePage(request):
    options = Option.objects.all()
    print(options) # колекции из джонго, похожи на список
    return render(request, "home.html", {'options': options})
# objects = это менеджер, репозиторий моделей

def buyPage(request, option_id):
    #return HttpResponse(f"You want to buy option {option_id}")
    option = Option.objects.get(pk = option_id)
    return render(request, 'subscribe.html', {'option': option})

def optionDetailPage(request, slug):
    #return HttpResponse(f"You want to buy option {option_id}")
    option = Option.objects.filter(slug=slug).first()
    return render(request, 'detail.html', {'option': option})


def payConfirmPage(request, subscription_id):
    subscription = Subscription.objects.get(pk = subscription_id)
    subscription.payed = True
    subscription.started = timezone.now()
    #subscription.started = datetime.now()
    subscription.save()
    client = Client.objects.get(pk = subscription.client_id)
    option = Option.objects.get(pk = subscription.option_id)
    price = Money.objects.get(pk = option.price_id)

    #   HW4: add details to message body: date, period, option name, price
    '''send_mail("Subscription activated",
          f"Your subscription was activated on date - {subscription.started}, period - {option.period}, name - {option.name}, price - {price.amount} {price.currency}",
          "John_Smith_012024@outlook.com",
          [subscription.client.email],
          fail_silently=False,      
          )'''
    #   HW4: add details to message body: date, period, option name, price, picture
    '''email = EmailMessage(
    'Subscription activated',
    f"Your subscription was activated on date - {subscription.started}, period - {option.period}, name - {option.name}, price - {price.amount} {price.currency}",
    "John_Smith_012024@outlook.com",
    [subscription.client.email]
)
    cur = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(cur, "subscription.webp")
    img_data = open(file, "rb")
    email.attach('subscription.webp', img_data.read()) # email.attach('subscription.webp', img_data.read(),  'image/png')
    email.send()'''
    # print(subscription.client.email)
    # HM3: render page
    return render(request, 'subscription.html', {'client': client, 'option': option})
    #return HttpResponse('Your subscription is Active!')

def subscribePage(request, option_id):
    option = Option.objects.get(pk=option_id)
    
    # HW2: first - find the client ?
    try:
        client = Client.objects.get(username = request.GET.get('username'))
    except Client.DoesNotExist:
        client = None
    if client == None:
        # HW1: add username + fullname
        fullname = request.GET.get('full-name')
        list = fullname.split()
        first_name = str(list[0])
        last_name = str(list[1])
        username = request.GET.get('username')
        password = request.GET.get('password')
        first_name = first_name
        last_name = last_name
        email = request.GET.get('email')
        phone = request.GET.get('phone')

        user = User.objects.create_user(username, email, password)
     

        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO app_client (user_ptr_id, phone) VALUES ({user.id}, '{phone}');")
        cursor.execute(f"UPDATE auth_user SET first_name = '{first_name}', last_name = '{last_name}' WHERE id = {user.id};")

        client = Client.objects.get(pk = user.id)

        #client = Client.objects.raw(f"INSERT INTO app_client (user_ptr_id, phone) VALUES ({user.id}, '{phone}');")

        #client = Client(
            #username = request.GET.get('username'),
            #password = request.GET.get('password'),
            #first_name = first_name,
            #last_name = last_name
            #email = request.GET.get('email'),
            #phone = request.GET.get('phone')
            #phone = phone
            #)
        #client.user_ptr_id = user.id
        #client.save()

    subscription = Subscription(
        client = client,
        option = option
        )
    subscription.save()

    # STRIPE

    price = stripe.Price.create(
        currency = option.price.currency,
        unit_amount = option.price.amount,
        #recurring={"interval": "month"},
        product_data = {"name": option.name},
    )
    link = stripe.PaymentLink.create(
        line_items = [{"price": price.id, "quantity": 1}],
        after_completion = {
            'type': 'redirect',
            'redirect': {
                'url': f'http://127.0.0.1:8000/payment-confirm/{subscription.id}'
            }
        }
    )
    return redirect(link.url)
    #return HttpResponse(link.url)
    #return HttpResponse('Subscription received')

def chatPage(request):
    if request.user.is_authenticated:
        # HWI: add another check - if the user has an active subscription
        # 1. request.user <-- user id / user
        # 2. load client by user.id
        # 3. load subscription for this client
        # 4. !!! filter subscriptions by payed or not
        client = Client.objects.get(pk = request.user.id)
        subscription = Subscription\
            .objects\
            .filter(client = client)\
            .filter(payed = True)\
            .first()

        if subscription != None:
            if subscription.started + timedelta(days=subscription.option.period) >= timezone.now():
                messages = Message.objects.filter(Q(sender = client) | Q(receiver = client)) # sent or received filter
                messages = messages.order_by('-sent')[:5]
                messages = list(reversed(messages))
                #messages = messages.reverse()
                for message in messages:
                    if message.type == 'reply':
                        message.body = markdown.markdown(message.body)
                print(messages)
        # TODO: filter - period
        # print("SUBSCRIPTION",subscriptions)
        #if subscriptions.exists():
                return render(request, 'chat.html', {'messages': messages,  "test": "<h1>this is a test</h1>" })
            else:
                return redirect("/login")
        else:
             return redirect("/login")
    else:
        return redirect("/login")

# HM*: you can still use builder pattern here
gpt_key = 'gpt_key'


def chatAction(request):
    body = request.POST["body"]
    bot = Bot.objects.get(pk=38)
    message = Message(type='message', sender = request.user, receiver = bot, body = body)
    message.save()

    headers = {"Authorization": f"Bearer {gpt_key}"}
    payload = {
        "model": "gpt-3.5-turbo",
        #"model": "dall-e-2",
        "messages": [
            {"role": "user", "content": message.body}
        ]
    }

    res = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    response = res.content.decode('utf-8')
    data = json.loads(response)
    print(response)
    print(data)
    if res.status_code == 200: 
        # print(data['choises'][0]['message']['content'])
        reply = Message(type='reply', sender = bot, receiver = request.user, body = data['choises'][0]['message']['content'])
        reply.save()
    else:
        print("ERROR GPT!")
    return redirect("/chat")

def loginPage(request):
    return render(request, 'login.html', {})

def loginAction(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/")
    else:
        return redirect("/login")

def signupPage(request):
    return render(request, 'signup.html', {})
