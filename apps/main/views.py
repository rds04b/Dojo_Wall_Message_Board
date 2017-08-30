from django.shortcuts import render, redirect
import django.contrib.sessions
from django.contrib import messages
from .models import User, Message, Comment

def index(request):
    return render(request, 'main/index.html')

def results(request):
    context = {
        "messages" : Message.objects.all().order_by("-created_at")[:10],
        "comments" : Comment.objects.all().order_by("created_at")[:10],
        "users" : User.objects.all(),
    }
    return render(request, 'main/result.html', context)

def create(request):
    if request.method =='POST':
        print request.POST['first_name']
        data = User.objects.validate_and_create(request.POST)
        user_email = request.POST['email']
        if user_email != '':
            info = User.objects.get(email=user_email)
            request.session['method'] = 'registered'
            request.session['id'] = info.id
            request.session['name'] =info.first_name

        for err in data:
            messages.error(request, err)
        return redirect('/')

    context = {
        "user" : request.POST['first_name'],
        "messages" : Message.objects.all().order_by("created_at")[:10],
        "comments" : Comment.objects.all().order_by("created_at")[:10],

    }
    return render(request, 'main/result.html', context)

def create_message(request):
    if request.method =='POST':
        valid, data = Message.objects.create_message(request.POST, request.session['id'])

        if not valid:
            for err in data:
                messages.error(request, err)

    return redirect('main:results')

def create_comment(request, id):
    if request.method =='POST':
        valid, data = Comment.objects.create_comment(request.POST, request.session['id'], id)

        if not valid:
            for err in data:
                messages.error(request, err)

    return redirect('main:results')

def like(request, id):
    message_like = Message.objects.get(id=id)
    message_like.like +=1
    message_like.save()
    return redirect('main:results')

def like_comment(request, id):
    comment_like = Comment.objects.get(id=id)
    comment_like.like +=1
    comment_like.save()
    return redirect('main:results')

def login(request):
    if request.method =='POST':
        valid, data = User.objects.login(request.POST)
        if valid:

            user_email = request.POST['email']
            if user_email != '':
                info = User.objects.get(email=user_email)
                request.session['method'] = 'logged in'
                request.session['id'] = info.id
                request.session['name'] =info.first_name
        if not valid:
            for err in data:
                messages.error(request, err)
            return redirect('/')

    context = {
            "user" : data,
            "messages" : Message.objects.all().order_by("created_at")[:10],
            "comments" : Comment.objects.all().order_by("created_at")[:10],
        }

    return render(request, 'main/result.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def most(request):
    context = {
        "most" : Message.objects.all().order_by("-like")[:10]
    }
    return render(request, 'main/popular.html', context)

def delete(request, id):
    request.method='POST'
    Message.objects.filter(id=id).delete()
    return redirect('main:results')

def delete_comment(request, id):
    request.method='POST'
    Comment.objects.filter(id=id).delete()
    return redirect('main:results')
