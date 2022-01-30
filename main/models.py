from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def signup_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        duplicate = User.objects.filter(email=postData['email'])
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valid email address."
        if len(duplicate) > 0:
            errors['email'] = "Email already exists. Please login instead!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Password confirmation must match the password."
        return errors
    
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        user = User.objects.filter(email=postData['email'])
        if len(postData['email']) < 1:
            errors['email'] = "Please enter an email address."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valid email address or password."
        elif len(user) == 0:
            errors['email'] = "Account doesn't exist. Please register first."
        return errors

class User(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=24)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Product(models.Model): # Item class
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to='img/')
    desc = models.TextField()
    users_who_like = models.ManyToManyField(User, related_name="products_liked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Order(models.Model): # Order Item Class
    product = models.ForeignKey(Product, related_name="orders", on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def total_price(self):
        return self.quantity * self.product.price

class Cart(models.Model): # Order Class
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    orders = models.ManyToManyField(Order, related_name="carts")
    started_at = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def final_total(self):
        total = 0
        for order_item in self.orders.all():
            total += order_item.total_price()
        return total
    
    def final_total_two(self):
        total = 0
        for order_item in self.orders.all():
            total += order_item.total_price()
        return "{0:.2f}".format(total / 100)

class Review(models.Model):
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)