import json

import sweetify
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from blogbackapp.models import *

# Create your views here.
from blogfrontapp.forms import *


@login_required
def home(request):
    if request.user.is_superuser:
        posts = Post.objects.order_by('-created_at')
        bloggers= Blogger.objects.order_by('-created_at')
        comments = Comment.objects.order_by('-created_at')
        social = MainSocialMedia.objects.all()
        categories = Category.objects.all()
        newsletter = Newsletter.objects.all()
        editorial_pick = EditorsPick.objects.all()
        likes = PostLike.objects.all()
        contactus = ContactUsEmployee.objects.all()
        context = {
            'mainpage': 'mainpage',
            'posts':posts,
            'bloggers':bloggers,
            'comments':comments,
            'social':social,
            'categories':categories,
            'newsletter':newsletter,
            'editorial_pick':editorial_pick,
            'likes':likes,
            'contactus':contactus
        }
        return render(request, 'back/index.html', context)


    else:
        user = request.user
        blogger= Blogger.objects.filter(user_ptr_id=user.id).first()
        posts = Post.objects.filter(blogger=blogger).order_by('-created_at')
        comments = Comment.objects.filter(post__blogger=blogger).order_by('-created_at')
        social = BloggerSocialMedia.objects.filter(blogger=blogger).order_by('-created_at')
        categories = Category.objects.all()
        likes = PostLike.objects.filter(post__blogger=blogger).all()
        editorial_pick = EditorsPick.objects.all()
        context = {
            'mainpage': 'mainpage',
            'posts': posts,
            'blogger': blogger,
            'comments': comments,
            'social': social,
            'categories': categories,
            # 'newsletter': newsletter,
            'editorial_pick': editorial_pick,
            'likes': likes,
        }
        return render(request, 'back/index.html', context)





@login_required
def category(request):
    context = {
        'categories': Category.objects.all()
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
            sweetify.error(request, 'Error', text='Category not added', persistent='Try Again')
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
            sweetify.error(request, 'Error', text='Category not Updated', persistent='Try Again')
    return redirect('BLOGBACK:category')


def deletecategory(request, category_id):
    c = Category.objects.filter(id=category_id).first()
    if c:
        c.delete()
        sweetify.success(request, 'Success', text='Category Deleted', persistent='Ok')
    else:
        sweetify.error(request, 'Error', text='Category not Deleted', persistent='Try Again')
    return redirect('BLOGBACK:category')


@login_required
def posts(request):
    b = Blogger.objects.filter(user_ptr_id=request.user.id).first()
    c = Category.objects.order_by("-created_at").all()

    context = {
        'myposts': Post.objects.filter(blogger=b).order_by('-created_at'),
        'allposts': Post.objects.order_by('-created_at'),
        'blogger': b,
        'categories': c,
    }
    return render(request, 'back/post.html', context)


@login_required
def bloggers(request):
    context = {
        'bloggers': Blogger.objects.order_by("-created_at").all()
    }
    return render(request, 'back/bloggers.html', context)


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
        blogger = Blogger.objects.filter(user_ptr_id=user.id).first()
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
        sweetify.error(request, 'Error', text='Post not Deleted', persistent='Try Again')
    return redirect('BLOGBACK:posts')


def post_delete(request, post_id):
    b = Post.objects.filter(id=post_id).first()
    if b:
        b.post_image.delete()
        b.delete()
        sweetify.success(request, 'Success', text='Post Deleted', persistent='Ok')
    else:
        sweetify.error(request, 'Error', text='Post not Deleted', persistent='Try Again')
    return redirect('BLOGBACK:posts')


def edit_post(request, post_id):
    b = Post.objects.filter(id=post_id).first()
    if request.method == 'POST':
        # user = request.user
        # blogger = Blogger.objects.filter(user_ptr_id = user.id).first()
        form = PostForm(request.POST, request.FILES, instance=b)
        category = request.POST.get('category')
        category_list = request.POST.getlist('category[]')
        description = request.POST.get('description')
        # post_image = request.FILES['post_image']
        post_image = request.FILES.get('post_image')
        title = request.POST.get('title')
        print(post_image)
        cat = Category.objects.filter(id=category).first()
        # p = PostForm(request.FILES, request.FILES)

        if form.is_valid():
            Post.objects.filter(id=b.id).update(
                slug=(title.lower()).replace(" ", "-")
            )
            form.save()
            if b and category_list:
                for cat in category_list:
                    categ = Category.objects.filter(id=cat).first()
                    if PostTags.objects.filter(post=b, category=categ).exists():
                        pt = PostTags.objects.filter(post=b, category=categ).first()
                        PostTags.objects.filter(id=pt.id).update(
                            category=categ,
                            post=b,
                        )
                    else:
                        PostTags.objects.create(category=categ, post=b, )

        sweetify.success(request, 'Success', text='Post Updated', persistent='Ok')
    else:
        sweetify.error(request, 'Error', text='Post not Updated', persistent='Try Again')
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
            context = {
                'status': "ACTIVE"
            }
        else:
            Post.objects.filter(id=id).update(
                post_verify='INACTIVE'
            )
            context = {
                'status': "INACTIVE"
            }

        return JsonResponse(context)


def edutorial_pick(request):
    posts = []
    allposts = EditorsPick.objects.filter(post__post_verify='ACTIVE', editor_status='ACTIVE').order_by('-created_at')
    for p in allposts:
        posts.append(p.post)
    context = {
        'title': 'Edutorial Pick',
        'allposts': posts,
    }
    return render(request, 'back/edutorials_pick.html', context)


@csrf_exempt
def add_edutorial_pick(request):
    global context
    if request.method == 'POST':
        id = request.POST.get('id')
        # status = request.POST.get('status')
        post = Post.objects.filter(id=id).first()
        if EditorsPick.objects.filter(post=post, editor_status='ACTIVE').exists():
            e_post = EditorsPick.objects.filter(post=post).last()
            if e_post:
                EditorsPick.objects.filter(id=e_post.id).update(
                    editor_status='INACTIVE'
                )
                context = {
                    'status': "INACTIVE"
                }
        else:
            EditorsPick.objects.create(
                editor_status='ACTIVE',
                post=post,
            )

            context = {
                'status': "ACTIVE"
            }

        return JsonResponse(context)


@csrf_exempt
def contactusread(request):
    global context
    if request.method == 'POST':
        id = request.POST.get('id')
        contact = ContactUsEmployee.objects.filter(id=id).first()
        if contact:
            if contact.status == "UNREAD":
                ContactUsEmployee.objects.filter(id=contact.id).update(
                    status='READ',
                )
                context = {
                    'status': "READ"
                }
                return JsonResponse(context)
            pass
        else:
            context = {
                'status': "UNREAD"
            }

    return JsonResponse(context)


def comments(request):
    user = request.user.id
    blogger = Blogger.objects.filter(user_ptr_id=user).first()
    list_category = []
    admin_list_category = []

    list_comment = []
    adminlist_comment = []

    commentss = Comment.objects.filter(post__blogger=blogger).order_by('-created_at')
    allcommentss = Comment.objects.order_by('-created_at')
    for c in commentss:
        list_category.append(c.post)

    for l in list(set(list_category)):
        lcom = Comment.objects.filter(post_id=l.id).order_by('-created_at').first()
        list_comment.append(lcom)

    for z in allcommentss:
        admin_list_category.append(z.post)

    for x in list(set(admin_list_category)):
        lcomm = Comment.objects.filter(post_id=x.id).order_by('-created_at').first()
        adminlist_comment.append(lcomm)

    # print(admin_list_category, adminlist_comment)
    # print(list_category, list_comment)
    context = {
        'title': 'Comments',
        'allposts': list(set(list_category)),
        'mylist': zip(list(set(list_category)), list(set(list_comment))),
        'myadminlist': zip(list(set(admin_list_category)), list(set(adminlist_comment))),
        'adminpost': list(set(admin_list_category))
    }
    return render(request, 'back/comments.html', context)


def social(request):
    blogger = Blogger.objects.filter(user_ptr_id=request.user.id).first()
    context = {
        'title': 'Social',
        'mainsocial': MainSocialMedia.objects.all(),
        'bloggerSocials': BloggerSocialMedia.objects.filter(blogger=blogger),
        'blogger': blogger,
        # 'allposts': list(set(list_category)),
        # 'mylist': zip(list(set(list_category)), list(set(list_comment))),
        # 'comments': list(set(list_comment))
    }
    return render(request, 'back/social.html', context)


def addsocial(request):
    if request.method == 'POST':
        form = MainSocialMediaForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Success', text='Social added', persistent='Ok')
        else:

            sweetify.error(request, 'Error', text='Error add social', persistent='Ok')

    return redirect(request.META['HTTP_REFERER'])


def updatesocial(request, social_id):
    social = MainSocialMedia.objects.filter(id=social_id).first()
    if request.method == "POST":
        form = MainSocialMediaForm(request.POST, instance=social)
        if form.is_valid():
            form.save()
            sweetify.success(request, "Success", text="Social updated", persistent='Ok')
        else:
            sweetify.error(request, "Error", text="Error updating social", persistent='Ok')
    return redirect(request.META["HTTP_REFERER"])


def deletesocial(request, social_id):
    social = MainSocialMedia.objects.filter(id=social_id).first()
    if social:
        social.delete()
        sweetify.success(request, "Success", text="Social deleted", persistent='Ok')
    else:
        sweetify.error(request, "Error", text="Error deleted social", persistent='Ok')

    return redirect(request.META["HTTP_REFERER"])


def userAccount(request):
    blogger = Blogger.objects.filter(user_ptr_id=request.user.id).first()
    context = {
        'title': 'UserAccount',
        'counties': County.objects.all(),
        'blogger': blogger,
        'categories': Category.objects.all()
    }
    return render(request, 'back/useraccount.html', context)


def updateuserdetails(request):
    if request.method == 'POST':
        newsletter = request.POST.get('newsletter')

        blogger = Blogger.objects.filter(user_ptr_id=request.user.id).first()
        form = BloggerFormUpdate(request.POST, request.FILES, instance=blogger)
        # print(newsletter)
        if form.is_valid():
            new_user = form.save()
            if newsletter is not None:
                if newsletter == 1:
                    # print(newsletter)
                    Newsletter.objects.create(
                        email=new_user.email
                    )
                elif newsletter == 0:
                    # print(newsletter)
                    n = Newsletter.objects.filter(email=new_user.email).first()
                    n.delete()

            sweetify.success(request, 'Success', text='Updated', persistent='Ok')

            return redirect('BLOGBACK:userAccount')
        else:

            sweetify.error(request, 'Error', text=form.errors.as_json(), persistent='Ok')

            return redirect('BLOGBACK:userAccount')


def updatemainuserdetails(request):
    if request.method == 'POST':
        user = User.objects.filter(id=request.user.id).first()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        emailname = request.POST.get('email')
        if user:
            User.objects.filter(id=user.id).update(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=emailname
            )

            sweetify.success(request, 'Success', text='Updated',
                             persistent='Ok')

            return redirect('BLOGBACK:userAccount')
        else:
            sweetify.error(request, 'Error', text='Error Updating User Account', persistent='Ok')

            return redirect('BLOGBACK:userAccount')


def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            sweetify.success(request, 'Success', text='Password Changed', persistent='Ok')
            return redirect(request.META['HTTP_REFERER'])
        else:
            print(form)
            l = []
            y = json.loads(form.errors.as_json())
            for k in y:
                l.append(
                    k + ' ' + y[k][0]['message']
                )
            print(l)
            sweetify.error(request, 'Error', text=l, persistent='Ok')
            return redirect(request.META['HTTP_REFERER'])

    else:
        sweetify.error(request, 'Error', text='Error Changing Password', persistent='Ok')
        return redirect(request.META['HTTP_REFERER'])


def newsletter(request):
    context = {
        'title': 'NewsLetter',
        'newsletter': Newsletter.objects.all(),
    }
    return render(request, 'back/newsletter.html', context)


def sendemail(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        subscribers = request.POST.getlist('subscribers[]')
        print(subject, message, subscribers)
        if subject and message and subscribers:
            from django.core.mail import send_mail
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, subscribers)
                sweetify.success(request, 'Success', text='Mails Sent', persistent='Ok')
            except Exception as ec:
                print(ec)
                sweetify.error(request, 'Error', text='Mails Not Sent', persistent='Ok')
    else:
        sweetify.error(request, 'Error', text='Mails Not Sent', persistent='Ok')
    return redirect(request.META['HTTP_REFERER'])


def del_newsletter(request, news_id):
    social = Newsletter.objects.filter(id=news_id).first()
    if social:
        social.delete()
        sweetify.success(request, "Success", text="Subscriber deleted", persistent='Ok')
    else:
        sweetify.error(request, "Error", text="Error deleted Subscriber", persistent='Ok')

    return redirect(request.META["HTTP_REFERER"])


def contact(request):
    context = {
        'contacts': ContactUsEmployee.objects.order_by('-created_at')
    }
    return render(request, 'back/contactus.html', context)