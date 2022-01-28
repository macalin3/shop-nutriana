from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
import re
from .models import User

def index(request):
    return render(request, "index.html")

def show_products(request):
    return render(request, "our_products.html")

def log_in(request):
    return render(request, "log_in.html")

def process_login(request):
    return render(request, "log_in.html")

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
