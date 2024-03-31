#from django.http import HttpResponse

#def homePage(request):
#    return HttpResponse("Home Page!")

#def signupPage(request):
#    return HttpResponse("Signup Page!")

from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import Option, Client, Subscription

import stripe
stripe.api_key = "stripe.api_key"

def homePage(request):
    options = Option.objects.all()
    print(options) # колекции из джонго, похожи на список
    return render(request, "home.html", {'options': options})
# objects = это менеджер, репозиторий моделей

def buyPage(request, option_id):
    #return HttpResponse(f"You want to buy option {option_id}")
    option = Option.objects.get(pk=option_id)
    return render(request, 'subscribe.html', {'option': option})

def payConfirmPage(request, subscription_id):
    subscription = Subscription.objects.get(pk=subscription_id)
    subscription.payed = True
    subscription.save()
    client = Client.objects.get(pk=subscription.client_id)
    option = Option.objects.get(pk=subscription.option_id)
    # HM3: render page
    return render(request, 'subscription.html', {'client': client, 'option': option})
    #return HttpResponse(f'Your subscription is Active!')

def subscribePage(request, option_id):
    option = Option.objects.get(pk=option_id)
    # HW1: add username + fullname
    fullname=request.GET.get('full-name')
    list=fullname.split()
    first_name=list[0]
    last_name=list[1]
    # HW2: first - find the client ?
    try:
        client = Client.objects.get(username=request.GET.get('username'))
    except Client.DoesNotExist:
        client = None
    if client == None:
        client = Client(
            username=request.GET.get('username'),
            first_name=first_name,
            last_name=last_name,
            email=request.GET.get('email'),
            phone=request.GET.get('phone')
            )
        client.save()
    subscription = Subscription(
        client = client,
        option = option
        )
    subscription.save()

    # STRIPE

    price = stripe.Price.create(
        currency=option.price.currency,
        unit_amount=option.price.amount,
        #recurring={"interval": "month"},
        product_data={"name": option.name},
    )
    link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}],
        after_completion = {
            'type': 'redirect',
            'redirect': {
                'url': f'http://127.0.0.1:8000/payment-confirm/{subscription.id}'
            }
        }
    )
    return redirect(link.url)
    #return HttpResponse(link.url)
    #return HttpResponse(f'Subscription received')

def signupPage(request):
    return render(request, 'signup.html', {})
