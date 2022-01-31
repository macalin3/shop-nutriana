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
    path('our-products/<int:productID>/add-to-cart', views.item_increment_cart),
    path('our-products/<int:productID>/remove-from-cart', views.item_decrement_cart),
]