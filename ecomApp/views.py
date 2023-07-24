from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .forms import Signupform

# Create your views here.

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

    Products = Product.objects.all()
    context = {'products':Products, 'cartItems':cartItems }
    return render(request,'store/store.html',context)
    

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}
        print('Cart:',cart)
    
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

        for i in cart:
            cartItems += cart[i]["quantity"]
        
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)


def checkout(request):  
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
        
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:',productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)


    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item wad added',safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transcation_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        Customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=Customer,complete=False)
        total = float(data['form']['total'])
        order.transcation_id = transcation_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = Customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )

    else:
        print('User is not logged in')


    return JsonResponse('Payment complete',safe=False)

def signup(request):
    if request.method == 'POST':
        form = Signupform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = Signupform()
    return render(request, 'store/signup.html', {'form': form})
