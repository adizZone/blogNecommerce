from django.shortcuts import render
from django.http import HttpResponse
from .models import product, contact, order, tracker
from math import ceil
import json
from django.core.mail import send_mail


def index(request):
    product_categories = product.objects.values('category', 'id')
    all_categories = []

    categories = {item['category'] for item in product_categories}
    for category in categories:
        prod=product.objects.filter(category=category)

        n = len(prod)
        n_slides = n//4 + ceil((n/4) - (n//4))

        all_categories.append([prod, range(1, n_slides), n_slides])

    parameters = {'products': all_categories}
    return render(request, 'index.html', parameters)


def search(request):
    query = request.GET.get("search", "")
    l=query.split(' ')
    print(l)
    product_categories = product.objects.values('category', 'id')
    all_categories = []

    categories = {item['category'] for item in product_categories}
    for category in categories:
        prod=product.objects.filter(category=category)
        prod2=[item for item in prod if searchMatch(l, item)]

        n = len(prod)
        n_slides = n//4 + ceil((n/4) - (n//4))

        if len(prod2)!=0:
            all_categories.append([prod2, range(1, n_slides), n_slides])

    parameters = {'products': all_categories}

    if len(all_categories)==0:
        return render(request, 'shop/search.html')
    return render(request, 'shop/index.html', parameters)

def searchMatch(query, item):
    matched = 0
    length=len(query)

    for words in query:
        words = words.lower()
        if words in item.product_name.lower() or words in item.SubCategory.lower() or words in item.category.lower() or words in item.description.lower():
            matched+=1

    if length==1:
        if matched>0:
            return True
    elif length==2:
        if matched>1:
            return True
    elif length==3:
        if matched>=2:
            return True
    elif length>3:
        if matched>=3:
            return True
    elif length==0:
        return True
    return False




def about(request):
    return render(request, 'shop/about.html')



def Tracker(request):
    params={}
    display_products=[]
    updates=[]
    check=0

    if request.method == 'POST':
        order_id = request.POST.get('trackingId', '')
        mobile = request.POST.get('mobile', '')

        if not order_id.isdigit():
            order_id = 0

        orders = order.objects.filter(placed_order_id=order_id, phone=mobile)

        products = product.objects.values('id')

        if len(orders)>0:
            temp = orders[0].order_ids
            temp = temp[1:-1].split(',')
            # print(type(temp), temp)
            string1=""
            
            l1=[]
            for i in temp:
                l2=i.split(':')
                l2[1]=l2[1][1:]
                l2[0],l2[1]=int(l2[0]), int(l2[1])
                l1.append(l2)
            # print(l1)

            for item in l1:
                prod = product.objects.filter(id=item[0])
                display_products.append([prod[0], item[1]])

            order_updates = tracker.objects.filter(tracker_id=order_id)
            for i in order_updates:
                updates.append(i)

        else:
            check=1
        
        params={'products': display_products, 'updates': updates, 'check': check}
    return render(request, 'shop/tracker.html', params)



def Contact(request):
    thank=0
    if request.method == 'POST':
        name=request.POST.get('name', '')
        email=request.POST.get('e-mail', '')
        phone=request.POST.get('phone', '')
        query=request.POST.get('query', '')

        message = contact(name=name, phone=phone, email=email, query=query)
        message.save()
        thank=1

        send_mail(f"{name}'s query, From my webcart", f'USER INFO -\nE-mail Address: {email}\n\nPhone Number: {phone}\n\nQuery: "{query}"', 'Sender_Email_Address', ["Receiver_Email_Address"], fail_silently=False)
         
    return render(request, 'shop/contact.html', {'thank': thank})




def productView(request, prod_id):
    prod=product.objects.filter(id=prod_id)
    return render(request, 'shop/prodview.html', {'product': prod[0]})



def checkout(request):
    product_ids = product.objects.values('id')

    cart_string=""
    if request.method=='GET':
        cart_string = request.GET.get('text', 'default')
    cart_list = cart_string.split(',')[0:-1]

    l1=[]
    l2=[]
    for i in cart_list:
        l3=i.split('=')

        l3[0]=int(l3[0])
        l1.append(l3[0])

        l3[1]=int(l3[1])
        l2.append(l3[1])
        

    products=[]
    for i in range(len(l1)):
        prod=product.objects.filter(id=l1[i])
        products.append([prod[0], l2[i]])


    placed_orders=str(dict(zip(l1,l2)))

    # database logic
    thank=0
    tracking_id=0

    if request.method=='POST':
        order_ids = request.POST.get('buyedItems', '')
        cost = request.POST.get('amount', 0)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        Address01 = request.POST.get('inputAddress' '')
        Address02= request.POST.get('inputAddress2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        phone = request.POST.get('mobile', '')
        pin_code = request.POST.get('pin_code', '')


        orders=order(order_ids=order_ids, cost=cost, name=name, email=email, Address01=Address01, Address02=Address02, city=city, state=state, phone=phone, pin_code=pin_code)

        orders.save()
        thank=1
        tracking_id=orders.placed_order_id

        Status=tracker(tracker_id=tracking_id, status="Your order has been placed successfully!")
        Status.save()

    params = {'placed_products': products, 'thank': thank, 'id': tracking_id, "placed_orders":placed_orders}
    return render(request, 'shop/checkout.html', params)



def cart(request):
    return render(request, 'shop/checkout.html')
