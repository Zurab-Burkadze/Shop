from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<int:product_id>', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>', views.delete_product, name='delete_product'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('delete_cart_item/<int:product_id>', views.delete_cart_item, name='delete_cart_item'),
]
