from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites, name='favorites'),
    path('product/', views.paginaProducto, name='product'),
    path('store/', views.store, name='store'),

    path('cart/', views.cart, name='cart'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),

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
    path('crud/viewproducts/deleteproduct/<str:pk>', views.deleteProduct, name='deleteproduct'),

    path('crud/view_orders/', views.view_orders, name='view_orders'),
    path('crud/view_orders/modify/<str:order_id>/', views.modify_order, name='modify_order'),
    path('crud/view_orders/delete/<str:order_id>/', views.delete_order, name='delete_order'),
]

