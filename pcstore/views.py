from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import customUserCreation, customUserChangeForm, passwordChangeForm
from .models import *
import datetime
from .forms import productForm
from django.http import Http404
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

#NO PUDE HACER QUE ESTA FUNCION get_object_or_404 FUNCIONARA ASIQUE BUSQUE EN INTERNET UNA PARECIDA
def custom_get_object_or_404(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        raise Http404(f"{klass.__name__} not found")


def inisesion(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            context = {
                "mensaje":"Usuario o contraseña incorrecta",
                "design":"alert alert-danger w-50 mx-auto text-center",
            }

            return render(request, 'login.html', context)
        
        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context = {
                "mensaje":"Usuario o contraseña incorrecta",
                "design":"alert alert-danger w-50 mx-auto text-center",
            }
    else:
        return render(request, 'login.html', context)
    
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')

def registrarse(request):
    form = UserCreationForm()
    context = {'form': form} 

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            context.update({
                "mensaje":"Ha ocurrido un error en el registro",
                "design":"alert alert-danger w-50 mx-auto text-center",
            })

    return render(request, 'register.html', context)

@staff_member_required
def createUser(request):
    if request.method == 'POST':
        form = customUserCreation(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            if role == 'superuser':
                user.is_staff = True
                user.is_superuser = True
            elif role == 'staff':
                user.is_staff = True
            user.save()
            return redirect('seeusers')
    else:
        form = customUserCreation()
    return render(request, 'createuser.html', {'form': form})

@staff_member_required
def changePassword(request, pk):
    user = custom_get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = passwordChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('seeusers')
    else:
        form = passwordChangeForm(instance=user)
    context = {'form': form,'user':user}
    return render(request, 'changeuserpassword.html', context)

def get_user_role(user):
    if user.is_superuser:
        return "Superuser"
    elif user.is_staff:
        return "Staff"
    else:
        return "Regular User"

@staff_member_required
def seeUsers(request):
    users = User.objects.all()
    for user in users:
        user.role = get_user_role(user)
    context = {'users': users}
    return render(request, 'seeusers.html', context)

@staff_member_required
def editUser(request, user_id):
    user = custom_get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = customUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('seeusers')
    else:
        form = customUserChangeForm(instance=user)

    context = {'form': form, 'user':user}
    return render(request, 'edituser.html', context)

@staff_member_required
def deleteUser(request,pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('seeusers')
    return render(request, 'deleteuser.html',{'obj':user})

def index(request):
    return render(request, 'index.html')

def favorites(request):
    return render(request, 'favorites.html')

def paginaProducto(request):
    return render(request, 'paginaproducto.html')

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items': items,'order':order}
    return render(request, 'cart.html', context)

def store(request):
    products = product.objects.all()
    context = {'products': products}
    return render(request, 'store.html', context)

@staff_member_required
def crudView(request):
    return render(request, 'crud.html')

@staff_member_required
def addProduct(request):
    form = productForm()
    if request.method == 'POST':
        form = productForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('viewproducts')
        else:
            print("Form errors:", form.errors) 

    context = {'form': form}
    return render(request, 'addproduct.html', context)

@staff_member_required
def updateProduct(request,pk):
    products = product.objects.get(id=pk)
    form = productForm(instance=products)
    
    if request.method == 'POST':
        form = productForm(request.POST, request.FILES, instance=products)
        if form.is_valid():
            form.save()
            return redirect('viewproducts')

    context = {'form': form}
    return render(request, 'updateproduct.html', context)

@staff_member_required
def viewProducts(request):
    products = product.objects.all()
    context = {'products': products}
    return render(request, 'viewproducts.html', context)

@staff_member_required
def deleteProduct(request,pk):
    producto = product.objects.get(id=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('viewproducts')
    return render(request, 'deleteproduct.html',{'obj':producto})

def update_item(request):
    try:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        print('Action:', action)
        print('Product ID:', productId)

        customer = request.user.customer
        prod = product.objects.get(id=productId)
        order , created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=prod)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
        
        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        context = {'message': 'Item was added'}
        return JsonResponse(context, safe=False)
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'error': str(e)}, status=500)
    except product.DoesNotExist:
        print("Product not found")
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Order.DoesNotExist:
        print("Order not found")
        return JsonResponse({'error': 'Order not found'}, status=404)
    except ValueError as ve:
        print("ValueError:", ve)
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'error': str(e)}, status=500)
    
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            comuna=data['shipping']['comuna'],
            zipcode=data['shipping']['zipcode'],
        )

        print(f"Order Details:\n"
              f"Transaction ID: {transaction_id}\n"
              f"Customer: {customer}\n"
              f"Order: {order}\n"
              f"Created: {created}\n"
              f"Total from form: {total}\n"
              f"Order total: {order.get_cart_total}\n"
              f"Order Complete: {order.complete}\n"
              f"Address: {data['shipping']['address']}\n"
              f"City: {data['shipping']['city']}\n"
              f"Comuna: {data['shipping']['comuna']}\n"
              f"Zipcode: {data['shipping']['zipcode']}\n")

    else:
        print('User is not logged in...')
    return JsonResponse('Payment complete', safe=False)