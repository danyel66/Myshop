from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from .tasks import payment_completed
from django.http import JsonResponse
from orders.forms import OrderCreateForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO

import stripe
stripe.api_key = "sk_test_co8XAgMCIPF7uAFZ9O5pWU2I00hX8N3CuH"



def index(request):
    return render(request, 'payment/index.html')

def charge(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    amount = int(request.POST['amount1'])

    if request.method == 'POST':
        print('Data:', request.POST)

        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['nickname'],
            source=request.POST['stripeToken']
            )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,
            currency="NGN",
            description="My First Test Charge (created for API docs)",
            )
        # mark the order as paid
        order.paid = True
        order.save()
        # launch asynchronous task
        payment_completed.delay(order.id)


    return redirect(reverse('payment:success', args=[amount]))

def success(request, args):
    amount = args
    return render(request, 'payment/success.html', {'amount': amount})

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
