from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from django.core.exceptions import ObjectDoesNotExist
regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class MessageManager(models.Manager):
    def create_message(self, data, creator_id):
        print data, "\n data exists"
        errors = []

        secret_message = data['message']
        if secret_message == '':
            errors.append('must enter a valid date')
            return(False, errors)

        else:
            user = User.objects.get(id=creator_id)
            dojo_message = Message.objects.create(
                message=data['message'],
                user_id= User.objects.get(id=creator_id)
                )
            return(True, dojo_message)

class UserManager(models.Manager):
    def validate_and_create(self, data):
        print data, "\n data exists"

        errors = []
        password = data['password'].encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        if len(data['first_name']) < 2:
            errors.append('first name is too short')
        if len(data['last_name']) < 2:
            errors.append('last name is too short')
        if not regex.match(data['email']):
            errors.append('email not valid')
        if len(data['password']) < 8:
            errors.append('email must be 8 characters long')
        if data['password'] != data['cpassword']:
            errors.append('password does not match')

        if errors != []:
            return(False, errors)
        try:
            user_email = data['email']
            registered_email = User.objects.get(email = user_email)
            if registered_email.email == user_email:
                errors.append('email already in use')
                return(False, errors)

        except:
            new_user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=hashed
            )
            return(True, new_user)

    def login(self, data):
        errors = []

        if not regex.match(data['email']):
            errors.append('invalid email address')
        if len(data['password']) < 8:
            errors.append('invalid password')
        if errors:
            return(False, errors)
        try:
            user_info = User.objects.get(email=data['email'])
            user_password = user_info.password
            if not bcrypt.checkpw(data['password'].encode(), user_password.encode()):
                errors.append('password incorrect')
        except ObjectDoesNotExist:
            errors.append('please register')
        if errors:
            return(False, errors)
        return(True, user_info.first_name)


class CommentManager(models.Manager):
    def create_comment(self, data, creator_id, post_id):
        print data, "\n data exists"
        errors = []

        user_comment = data['comment']
        if user_comment == '':
            errors.append('must enter a valid comment')
            return(False, errors)

        else:
            user = User.objects.get(id=creator_id)
            dojo_comment = Comment.objects.create(
                comment=data['comment'],
                user_id= User.objects.get(id=creator_id),
                message=Message.objects.get(id=post_id)
                )
            return(True, dojo_comment)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Message(models.Model):
    message = models.TextField(max_length=1000)
    like = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, related_name="dojo_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

class Comment(models.Model):
    comment = models.TextField(max_length=500)
    like = models.IntegerField(default=0)
    message = models.ForeignKey(Message)
    user_id = models.ForeignKey(User, related_name="dojo_comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()
