from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
import re
from .models import User, Product, Order, Cart, Review

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

def show_products(request):
    return render(request, "our_products.html")

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

    context = {
        "product": Product.objects.get(id=productID),
    }
    return render(request, "view_product.html", context)

def sign_out(request):
    del request.session['user_id']
    return redirect('/')