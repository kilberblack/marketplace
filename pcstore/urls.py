from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites, name='favorites'),
    path('product/', views.product, name='product'),
    path('filter/', views.filter, name='filter')
]
