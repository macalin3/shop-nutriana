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

class User(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=24)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
