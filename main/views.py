from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import bcrypt
import re
from .models import User, Product, Order, Cart, Review
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone 

def index(request):

    if not request.session.get('user_id'):

        context = {
            "all_products": Product.objects.all(),
        }

        return render(request,"index.html", context)
    
    else:

        context = {
            "all_products": Product.objects.all(),
            "current_user": User.objects.get(id=request.session['user_id']),
        }

        return render(request, "index.html", context)

def log_in(request):
    return render(request, "log_in.html")

def process_login(request):

    user_matching_email = User.objects.filter(email=request.POST['email']).first()
    # print(user_matching_email)
    if user_matching_email is not None:
        print(bcrypt.checkpw(request.POST['password'].encode(), user_matching_email.password.encode()))
        # print(f'*{user_matching_email.password}*')
        if bcrypt.checkpw(request.POST['password'].encode(), user_matching_email.password.encode()):
            # print('bcrypt=true')
            request.session['user_id'] = user_matching_email.id
            return redirect('/')
        else:
            messages.error(request, "Please enter a valid email address or password.")
            return redirect('/')
        
    errors = User.objects.login_validator(request.POST)

    # validate User (see login_validator funcion in models.Manager)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/log-in')

def sign_up(request):
    return render(request, "sign_up.html")

def process_signup(request):

    errors = User.objects.signup_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/sign-up')

    else:
        user = User()
        user.email = request.POST['email']
        user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user.save()
        request.session['user_id'] = user.id
        return redirect("/")

def view_product(request, productID):

    try:
        order = Cart.objects.get(user=User.objects.get(id=request.session['user_id']))

        context = {
            "product": Product.objects.get(id=productID),
            "current_user": User.objects.get(id=request.session['user_id']),
            "object": order,
        }
        return render(request, "view_product.html", context)
    
    except ObjectDoesNotExist:
        context = {
            "product": Product.objects.get(id=productID),
            "current_user": User.objects.get(id=request.session['user_id']),
        }

        return render(request, 'view_product.html', context)

def sign_out(request):
    del request.session['user_id']
    return redirect('/')

def add_favorite(request, productID):
    this_product = Product.objects.get(id=productID)
    this_user = User.objects.get(id=request.session['user_id'])
    this_user.products_liked.add(this_product)
    print('success!')
    return redirect(f'/our-products/{productID}')    

def remove_favorite(request, productID):
    this_product = Product.objects.get(id=productID)
    this_user = User.objects.get(id=request.session['user_id'])
    this_user.products_liked.remove(this_product)
    return redirect(f'/our-products/{productID}')

def item_increment(request, productID):
    item = get_object_or_404(Product, id=productID)
    current_user = User.objects.get(id=request.session['user_id'])
    order_item, created = Order.objects.get_or_create(
        product=item,
        user=current_user,
        ordered=False
    )
    inquiry = Cart.objects.filter(user=current_user,ordered=False)
    if inquiry.exists():
        order = inquiry[0]
        if order.orders.filter(product_id=productID).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Successfully added to your cart!")
            return redirect(f'/our-products/{productID}')

        else:
            order.orders.add(order_item)
            messages.info(request, "Successfully added to your cart!")
            return redirect(f'/our-products/{productID}')
    else:
        ordered_date = timezone.now()
        order = Cart.objects.create(
            user=current_user,
            ordered_date=ordered_date
        )
        order.orders.add(order_item)
        messages.info(request, "Successfully added to your cart!")
        return redirect(f'/our-products/{productID}')

def item_decrement(request, productID):
    item = Product.objects.get(id=productID)
    current_user = User.objects.get(id=request.session['user_id'])
    inquiry = Cart.objects.filter(user=current_user,ordered=False)
    if inquiry.exists():
        order = inquiry[0]
        if order.orders.filter(product_id=productID).exists():
            order_item = Order.objects.filter(
                product=item,
                user=current_user,
                ordered=False
            )[0]
            order.orders.remove(order_item)
            order_item.delete()
            messages.info(request, "Successfully removed from your cart!")
            return redirect(f'/our-products/{productID}')
        else:
            # messages.info(request, "This item was not in your cart.")
            return redirect(f'/our-products/{productID}')
    else:
        # messages.info(request, "You do not have an active order.")
        return redirect(f'/our-products/{productID}')

def item_increment_cart(request, productID):
    item = get_object_or_404(Product, id=productID)
    current_user = User.objects.get(id=request.session['user_id'])
    order_item, created = Order.objects.get_or_create(
        product=item,
        user=current_user,
        ordered=False
    )
    inquiry = Cart.objects.filter(user=current_user,ordered=False)
    if inquiry.exists():
        order = inquiry[0]
        if order.orders.filter(product_id=productID).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect('/cart')

        else:
            order.orders.add(order_item)
            return redirect('/cart')
    else:
        ordered_date = timezone.now()
        order = Cart.objects.create(
            user=current_user,
            ordered_date=ordered_date
        )
        order.orders.add(order_item)
        return redirect('/cart')

def item_decrement_cart(request, productID):
    item = Product.objects.get(id=productID)
    current_user = User.objects.get(id=request.session['user_id'])
    inquiry = Cart.objects.filter(user=current_user,ordered=False)
    if inquiry.exists():
        order = inquiry[0]
        if order.orders.filter(product_id=productID).exists():
            order_item = Order.objects.filter(
                product=item,
                user=current_user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                
            else:
                order.orders.remove(order_item)
            return redirect('/cart')
        else:
            order.orders.remove(order_item)
            messages.info(request, "This item was not in your cart")
            return redirect('/cart')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('/cart')

def show_products(request):
    
    if not request.session.get('user_id'):

        context = {
            "all_products": Product.objects.all(),
        }

        return render(request,"our_products.html", context)
    
    else:

        context = {
            "all_products": Product.objects.all(),
            "current_user": User.objects.get(id=request.session['user_id']),
        }

        return render(request, "our_products.html", context)

def show_about(request):
    pass

def show_contact(request):
    pass

def show_cart(request):

    try:
            
        order = Cart.objects.get(user=User.objects.get(id=request.session['user_id']))
        context = {
            "current_user": User.objects.get(id=request.session['user_id']),
            "object": order,
                
        }
        return render(request, 'cart.html', context)
        
    except ObjectDoesNotExist:
        context = {
            "current_user": User.objects.get(id=request.session['user_id']),
        
        }
        return render(request, 'cart.html', context)

def item_trash(request, productID):
    item = Product.objects.get(id=productID)
    current_user = User.objects.get(id=request.session['user_id'])
    inquiry = Cart.objects.filter(user=current_user,ordered=False)
    if inquiry.exists():
        order = inquiry[0]
        if order.orders.filter(product_id=productID).exists():
            order_item = Order.objects.filter(
                product=item,
                user=current_user,
                ordered=False
            )[0]
            order.orders.remove(order_item)
            order_item.delete()
            return redirect("/cart")
        else:
            return redirect("/cart")
    else:
        return redirect("/cart")