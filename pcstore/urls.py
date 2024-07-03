from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites, name='favorites'),
    path('product/', views.product, name='product'),
    path('filter/', views.filter, name='filter'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.inisesion, name='inisesion'),
    path('register/', views.registrarse, name='registro')
]
