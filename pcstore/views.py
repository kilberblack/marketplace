from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def favorites(request):
    return render(request, 'favorites.html')

def product(request):
    return render(request, 'product.html')

def filter(request):
    return render(request, 'filter.html')

def cart(request):
    return render(request, 'cart.html')

def inisesion(request):
    return render(request, 'login.html')

def registrarse(request):
    return render(request, 'register.html')