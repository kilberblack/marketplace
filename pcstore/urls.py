from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites, name='favorites'),
    path('product/', views.paginaProducto, name='product'),
    path('filter/', views.filter, name='filter'),
    path('cart/', views.cart, name='cart'),

    path('login/', views.inisesion, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registrarse, name='registro'),

    path('crud/', views.crudView, name='crud'),

    path('crud/seeusers/', views.seeUsers, name='seeusers'),
    path('crud/seeusers/createuser/', views.createUser, name='createuser'),
    path('crud/seeusers/edituser/<str:user_id>', views.editUser, name='edituser'),
    path('crud/seeusers/deleteuser/<str:pk>', views.deleteUser, name='deleteuser'),
    path('crud/seeusers/changeuserpassword/<str:pk>', views.changePassword, name='changeuserpassword'),

    path('crud/viewproducts/', views.viewProducts, name='viewproducts'),
    path('crud/viewproducts/addproduct/', views.addProduct, name='addproduct'),
    path('crud/viewproducts/updateproduct/<str:pk>', views.updateProduct, name='updateproduct'),
    path('crud/viewproducts/deleteproduct/<str:pk>', views.deleteProduct, name='deleteproduct')
]
