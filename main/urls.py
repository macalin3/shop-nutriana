from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('our-products', views.show_products),
    path('log-in', views.log_in),
    path('process-login', views.process_login),
    path('sign-up', views.sign_up),
    path('process-signup', views.process_signup),
    path('our-products/<int:productID>', views.view_product),
    path('sign-out', views.sign_out),
    path('our-products/<int:productID>/favorite', views.add_favorite),
    path('our-products/<int:productID>/unfavorite', views.remove_favorite),
    path('cart/item_increment/<int:productID>/add', views.item_increment_cart, name='item_increment_cart'),
    path('cart/item_decrement/<int:productID>/remove', views.item_decrement_cart, name='item_decrement_cart'),
    path('about-nutriana', views.show_about),
    path('contact-nutriana', views.show_contact),
    path('our-products/<int:productID>/add-to-order', views.item_increment),
    path('our-products/<int:productID>/remove-from-order', views.item_decrement),
    path('cart', views.show_cart),
    path('cart/item_decrement/<int:productID>/trash', views.item_trash, name='item_trash'),
]