import json
from . models import *

def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart: ',cart)
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            prod = product.objects.get(id=i)
            total = (prod.precio * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id': prod.id,
                    'nombre': prod.nombre,
                    'precio': prod.precio,
                    'imageURL': prod.imageURL
                    },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
        except:
            pass
    return {'items': items,'order':order, 'cartItems': cartItems}

def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            order = Order.objects.get(customer=customer, complete=False)
        except Order.MultipleObjectsReturned:
            orders = Order.objects.filter(customer=customer, complete=False)
            order = orders.first()
            for extra_order in orders[1:]:
                for item in extra_order.orderitem_set.all():
                    item.order = order
                    item.save()
                extra_order.delete()
        except Order.DoesNotExist:
            order = Order.objects.create(customer=customer, complete=False)

        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookie_cart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'items': items,'order':order, 'cartItems': cartItems}

def guest_order(request, data):
    print('User is not logged in...')
    print('COOKIES:', request.COOKIES)

    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookie_cart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer,complete=False)

    for item in items:
        prod = product.objects.get(id=item['product']['id'])
        OrderItem.objects.create(product=prod, order=order, quantity=item['quantity'])

    return customer, order