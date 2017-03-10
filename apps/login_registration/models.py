from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt
import re

# regex to test whether given name contains letters only and is at least 3 characters long
name_regex = re.compile(r'[A-Za-z]{3,}')
# regex to test whether given email is valid
email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-z]*$')
# regex to test whether given password is at least 8 characters long
password_regex = re.compile(r'(?=.{8,})')
# regex to test whether given date is in valid MM/DD/YYYY format
date_regex = re.compile(r'\d{1,2}\/\d{1,2}\/\d{4}')

class UserManager(models.Manager):
    def register(self, postData):
        # runs validation test
        errors = self.validate(postData)
        # creates a hashed password
        # and stores user information into a new User object
        if not errors:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            birthdate = datetime.strptime(postData['birthdate'], '%m/%d/%Y')
            user = User.objects.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=hashed_password,
                birthdate=birthdate
            )
            return user
        else:
            return errors

    # searches for Users matching the given email and tests whether the given
    # password matches the stored password
    def login(self, postData):
        user = User.objects.filter(email=postData['email'])
        if not user:
            return False
        if bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) != user[0].password.encode():
            return False
        else:
            return user[0]

    # deletes the session attached to the given user id
    def logout(self, session):
        del session
        return True

    # tests whether given user first name, last name, email, and password
    # are all valid
    def validate(self, postData):
        errors = []
        try:
            user = User.objects.get(email=postData['email'])
            errors.append("User email already exists! Please log in!")
        except:
            if not re.match(name_regex, postData['first_name']):
                errors.append("First name must be more than 2 characters!")
            if not re.match(name_regex, postData['last_name']):
                errors.append("Last name must be more than 2 characters!")
            if not re.match(email_regex, postData['email']):
                errors.append("Email address is invalid!")
            if not re.match(password_regex, postData['password']):
                errors.append("Password is invalid!")
            elif postData['password'] != postData['confirm_password']:
                errors.append("Passwords do not match!")
            if not re.match(date_regex, postData['birthdate']):
                errors.append("Birthdate must be in MM/DD/YYYY format!")
            else:
                birthdate = datetime.strptime(postData['birthdate'], '%m/%d/%Y')
                today = datetime.now()
                today = datetime.replace(today, hour=0, minute=0, second=0, microsecond=0)
                if birthdate >= today:
                    errors.append("Birthdate cannot be on or after today!")
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
