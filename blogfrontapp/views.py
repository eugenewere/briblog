import json
import os

import sweetify
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from blogfrontapp.forms import *

def getCounties():
    mod = os.path.dirname(__file__)
    file = os.path.join(mod, 'county.json')
    with open(file) as f:
        data = f.read()
        # print(data.split('¿', 1)[1])
        json_data = json.loads(data.split('¿', 1)[1])

        for p in json_data:
            County.objects.create(
                county_number=p['county_number'],
                county=p['county'],
            )
            # print(p['county_number'], p['county'])

def home(request):
    posts = Post.objects.order_by('-created_at')
    context = {
        'title': 'Home',
        'allposts':posts,
    }
    return render(request, 'bnews/index.html', context)


def timeline(request):
    context = {
        'title': 'Timeline',
    }
    return render(request, 'bnews/timeline.html', context)


def contact(request):
    context = {
        'title': 'Contact',
    }
    return render(request, 'bnews/contact.html', context)


def register(request):
    context = {
        'title': 'Register',
        'counties':County.objects.all()
    }

    return render(request, 'bnews/register.html', context)


def singleblog(request):
    context = {
        'title': 'Singleblog',
    }
    return render(request, 'bnews/register.html', context)


def blogs(request):
    context = {
        'title': 'Blogs',
    }
    return render(request, 'bnews/blogs.html', context)

@login_required
def logout_user(request):
    user = request.user
    if user:
        logout(request)
        return redirect('BLOG:home')


def makeregister(request):
    if request.method == 'POST':
        newsletter = request.POST.get('newsletter')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        print(newsletter)
        form = BloggerForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            if newsletter is not None:
                Newsletter.objects.create(
                   email=new_user.email
                )
            new_userrr = authenticate(username=username, password=password1)
            login(request, new_userrr)
            data = {
                'results': 'success',
                'success': 'Good job! You successfully Registered and logged in'
            }
            return JsonResponse(data, safe=False)
        else:
            data = {
                'results': 'error',
                'form': form.errors.as_json(),
            }
            return JsonResponse(data)


def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        def usernamel(email):
            uz = User.objects.filter(email__exact=email).first()
            # us = User.objects.filter(email=uz.email).values('username').first()
            print(uz.email)
            print(uz.username)

            if uz.email:
                return uz.username
            return None

        if User.objects.filter(username__exact=username).first() or User.objects.filter(email__exact=username).first():
            if User.objects.filter(username__exact=username).first():

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_active and user.is_superuser:
                        login(request, user)
                        sweetify.success(request, title='Welcome Admin', text='Welcome Back', persistent='Continue', timer=1500)
                        return redirect('BLOGBACK:home')
                    if user.is_active:
                        if Blogger.objects.filter(user_ptr_id=user.id, group_status='VIEWER', is_user_active='ACTIVATE').exists():
                            login(request, user)
                            sweetify.success(request, title='Welcome',text='You successfully Logged in.', persistent="Ok", timer=1500)
                            return redirect('BLOG:home')
                        elif Blogger.objects.filter(user_ptr_id=user.id, group_status='BLOGGER', is_user_active="ACTIVATE").exists():
                            login(request, user)
                            sweetify.success(request, title='Welcome ', text='Welcome Back', persistent='Continue', timer=1500)
                            return redirect('BLOGBACK:home')
                        else:
                            sweetify.error(request, 'Error', text='Account Suspended. Contact Admin', persistent='Retry')
                            return redirect(request.META['HTTP_REFERER'])
                else:
                    sweetify.error(request, 'Error', text='Invalid Username and Password', persistent='Retry')
                    return redirect(request.META['HTTP_REFERER'])
            if User.objects.filter(email__exact=username).first():

                user = authenticate(request, username=usernamel(username), password=password)
                if user is not None:
                    if user.is_active and user.is_superuser:
                        login(request, user)
                        sweetify.success(request, title='Welcome Admin', text='Welcome Back', persistent='Ok',
                                         timer=1500)
                        return redirect('BLOGBACK:home')
                    if user.is_active:
                        if Blogger.objects.filter(user_ptr_id=user.id, group_status='VIEWER', is_user_active='ACTIVATE').exists():
                            login(request, user)
                            sweetify.success(request, title='Welcome', text='You successfully Logged in.',
                                             persistent='Continue', timer=1500)
                            return redirect('BLOG:home')
                        elif Blogger.objects.filter(user_ptr_id=user.id, group_status='BLOGGER', is_user_active='ACTIVATE').exists():
                            login(request, user)
                            sweetify.success(request, title='Welcome ', text='Welcome Back',
                                             persistent='Continue',
                                             timer=1500)
                            return redirect('BLOGBACK:home')
                        else:
                            sweetify.error(request, 'Error', text='Account Suspended. Contact Admin', persistent='Retry')
                            return redirect(request.META['HTTP_REFERER'])
                else:
                    sweetify.error(request, 'Error', text='Invalid Email and Password', persistent='Retry')
                    return redirect(request.META['HTTP_REFERER'])
        else:
            sweetify.error(request, 'Error', text='Invalid Credentials dont exist', persistent='Retry')
            return redirect(request.META['HTTP_REFERER'])
    return redirect(request.META['HTTP_REFERER'])