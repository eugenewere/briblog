import sweetify
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from blogbackapp.models import *



# Create your views here.
from blogfrontapp.forms import *


@login_required
def home(request):
    context={
        'mainpage':'mainpage',
    }
    return render(request,'back/index.html', context)

@login_required
def category(request):
    context={
        'categories':Category.objects.all()
    }
    return render(request, 'back/categories.html', context)
def addcategory(request):
    if request.method == 'POST':
        categoryy = request.POST.get('category')
        if categoryy:
            if not Category.objects.filter(category__exact=categoryy).exists():
                Category.objects.create(
                    category=categoryy
                )
                sweetify.success(request, 'Success', text='Category added', persistent='Ok')
            else:
                sweetify.error(request, 'Error', text='Category exists', persistent='Ok')
        else:
            sweetify.success(request, 'Error', text='Category not added', persistent='Try Again')
    return redirect('BLOGBACK:category')


def editcategory(request, category_id):

    if request.method == 'POST':
        c = Category.objects.filter(id=category_id).first()
        categoryy = request.POST.get('category')
        if categoryy:
            Category.objects.filter(id=c.id).update(
                category=categoryy
            )
            sweetify.success(request, 'Success', text='Category Updated', persistent='Ok')
        else:
            sweetify.success(request, 'Error', text='Category not Updated', persistent='Try Again')
    return redirect('BLOGBACK:category')


def deletecategory(request, category_id):

    c = Category.objects.filter(id=category_id).first()
    if c:
        c.delete()
        sweetify.success(request, 'Success', text='Category Deleted', persistent='Ok')
    else:
        sweetify.success(request, 'Error', text='Category not Deleted', persistent='Try Again')
    return redirect('BLOGBACK:category')

@login_required
def posts(request):
    b = Blogger.objects.filter(user_ptr_id=request.user.id).first()
    c = Category.objects.order_by("-created_at").all()

    context={
        'myposts':Post.objects.filter(blogger=b).order_by('-created_at'),
        'allposts':Post.objects.order_by('-created_at'),
        'blogger': b,
        'categories':c,
    }
    return render(request,'back/post.html', context)

@login_required
def bloggers(request):
    context ={
        'bloggers':Blogger.objects.order_by("-created_at").all()
    }
    return render(request,'back/bloggers.html', context)
def bloggers_group_status(request, blogger_id):
    blogger = Blogger.objects.filter(id=blogger_id).first()
    if blogger.group_status == 'BLOGGER':
        Blogger.objects.filter(id=blogger.id).update(
            group_status='VIEWER'
        )
        sweetify.success(request, 'Success', text='Group Status Changed', persistent='Ok')
    elif blogger.group_status == 'VIEWER':
        Blogger.objects.filter(id=blogger.id).update(
            group_status='BLOGGER'
        )
        sweetify.success(request, 'Success', text='Group Status Changed', persistent='Ok')
    return redirect('BLOGBACK:bloggers')
def bloggers_active_status(request, blogger_id):
    blogger = Blogger.objects.filter(id=blogger_id).first()
    if blogger.is_user_active == 'ACTIVATE':
        Blogger.objects.filter(id=blogger.id).update(
            is_user_active='DEACTIVATE'
        )
        sweetify.success(request, 'Success', text='Active Status Changed', persistent='Ok')
    elif blogger.is_user_active == 'DEACTIVATE':
        Blogger.objects.filter(id=blogger.id).update(
            is_user_active='ACTIVATE'
        )
        sweetify.success(request, 'Success', text='Active Status Changed', persistent='Ok')
    return redirect('BLOGBACK:bloggers')
def bloggers_delete(request, blogger_id):
    b = Blogger.objects.filter(id=blogger_id).first()
    if b:
        b.delete()
        sweetify.success(request, 'Success', text='Blogger Deleted', persistent='Ok')
    else:
        sweetify.success(request, 'Error', text='Blogger not Deleted', persistent='Try Again')
    return redirect('BLOGBACK:bloggers')


def addposts(request):
    if request.method == 'POST':
        user = request.user
        blogger = Blogger.objects.filter(user_ptr_id = user.id).first()
        category = request.POST.get('category')
        category_list = request.POST.getlist('category[]')
        description = request.POST['description']
        post_image = request.FILES.get('post_image')
        title = request.POST.get('title')
        # print(blogger,category, category_list,description,post_image,title)
        print(post_image)
        cat = Category.objects.filter(id=category).first()
        p = Post.objects.create(
            blogger=blogger,
            post_image=post_image,
            category=cat,
            description=description,
            title=title
        )
        if p and category_list:
            for cat in category_list:
                categ = Category.objects.filter(id=cat).first()
                PostTags.objects.create(
                    category=categ,
                    post=p,
                )


        sweetify.success(request, 'Success', text='Post Added', persistent='Ok')
    else:
        sweetify.success(request, 'Error', text='Post not Deleted', persistent='Try Again')
    return redirect('BLOGBACK:posts')


def post_delete(request, post_id):
    b  = Post.objects.filter(id=post_id).first()
    if b:
        b.post_image.delete()
        b.delete()
        sweetify.success(request, 'Success', text='Post Deleted', persistent='Ok')
    else:
        sweetify.success(request, 'Error', text='Post not Deleted', persistent='Try Again')
    return redirect('BLOGBACK:posts')


def edit_post(request, post_id):
    b  = Post.objects.filter(id=post_id).first()
    if request.method == 'POST':
        # user = request.user
        # blogger = Blogger.objects.filter(user_ptr_id = user.id).first()
        category = request.POST.get('category')
        category_list = request.POST.getlist('category[]')
        description = request.POST.get('description')
        post_image = request.FILES['post_imageb']
        title = request.POST.get('title')
        print(post_image)
        # print(blogger,category, category_list,description,post_image,title)
        cat = Category.objects.filter(id=category).first()
        # p = PostForm(request.FILES, request.FILES)
        p = Post.objects.filter(id=b.id).update(
            # post_image='post_image/'+str(post_image),
            category=cat,
            description=description,
            title=title,
            post_image=post_image,
        )
        if p and category_list:
            for cat in category_list:
                categ = Category.objects.filter(id=cat).first()
                if PostTags.objects.filter(post=b, category=categ).exists():
                    pt = PostTags.objects.filter(post=b, category=categ).first()
                    PostTags.objects.filter(id=pt.id).update(
                        category=categ,
                        post=b,
                    )
                else:
                    PostTags.objects.create(
                        category=categ,
                        post=b,
                    )

        sweetify.success(request, 'Success', text='Post Updated', persistent='Ok')
    else:
        sweetify.success(request, 'Error', text='Post not Updated', persistent='Try Again')
    return redirect('BLOGBACK:posts')

@csrf_exempt
def edit_post_status(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        # status = request.POST.get('status')
        if Post.objects.filter(id=id, post_verify='INACTIVE'):
            Post.objects.filter(id=id).update(
                post_verify='ACTIVE'
            )
            context={
                'status':"ACTIVE"
            }
        else:
            Post.objects.filter(id=id).update(
                post_verify='INACTIVE'
            )
            context = {
                'status': "INACTIVE"
            }

        return JsonResponse(context)

