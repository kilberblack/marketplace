from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def favorites(request):
    return render(request, 'favorites.html')

def product(request):
    return render(request, 'product.html')

def filter(request):
    return render(request, 'filter.html')