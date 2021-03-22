import json
import os

import sweetify
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Min, Max
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from hitcount.views import HitCountDetailView
# import pyshorteners
from blogfrontapp.forms import *
from django.db.models import Q

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
    posts = Post.objects.filter(post_verify="ACTIVE").order_by('?')
    context = {
        'title': 'Home',
        'allposts': posts,
    }
    return render(request, 'bnews/index.html', context)


def timeline(request):
    if request.method == "POST":
        datefrm = request.POST.get('dateFrom')
        dateto = request.POST.get('dateTo')

        from datetime import datetime
        first_date = datetime.date(datetime.strptime(datefrm, "%Y-%M-%d"))
        last_date = datetime.date(datetime.strptime(dateto, "%Y-%M-%d"))
        posts = Post.objects.filter(created_at__gte=first_date, created_at__lte=last_date, post_verify="ACTIVE").order_by('-created_at')
        print(posts)
        print(dateto, dateto)
        dates = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        context = {
            'date_range': str(dates[first_date.month]) +' '+str(first_date.year)+'  -  '+str(dates[last_date.month]) +' '+str(last_date.year),
            'title': 'Timeline',
            'posts': posts,
        }
        return render(request, 'bnews/timeline.html', context)
    else:
        context = {
            'title': 'Timeline',
            'posts': Post.objects.filter(post_verify="ACTIVE").order_by('-created_at')
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
        'counties': County.objects.all()
    }

    return render(request, 'bnews/register.html', context)


class PostDetailView(HitCountDetailView):
    model = Post
    template_name = 'bnews/singleblog.html'
    context_object_name = 'post'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        post = Post.objects.filter(id=self.kwargs['post_id']).first()
        similar_posts = Post.objects.filter(category=post.category, post_verify="ACTIVE").all()
        blogger = Blogger.objects.filter(user_ptr_id=self.request.user.id).first()
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(post=post, reply__isnull=True).order_by('-created_at')
        socials = BloggerSocialMedia.objects.filter(blogger=blogger).all()
        context.update({
            'socials':socials,
            'title': post.title,
            'comments':comments,
            'post': post,
            'similar_posts': similar_posts,
            'blogger': blogger,
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context


def get_next_id(curr_id):
    try:
        ret = Post.objects.filter(id__gt=curr_id, post_verify='ACTIVE').order_by("id")[0:1].get().id
    except Post.DoesNotExist:
        ret = Post.objects.aggregate(Min("id"))['id__min']
    return ret


def get_prev_id(curr_id):
    try:
        ret = Post.objects.filter(id__lt=curr_id, post_verify='ACTIVE').order_by("-id")[0:1].get().id
    except Post.DoesNotExist:
        ret = Post.objects.aggregate(Max("id"))['id__max']
    return ret


class NextPostDetailView(HitCountDetailView):
    model = Post
    template_name = 'bnews/singleblog.html'
    context_object_name = 'post'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        post = Post.objects.filter(id=get_next_id(self.kwargs['post_id'])).first()
        similar_posts = Post.objects.filter(category=post.category, post_verify="ACTIVE").all()
        blogger = Blogger.objects.filter(user_ptr_id=self.request.user.id).first()
        context = super(NextPostDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(post=post, reply__isnull=True).order_by('-created_at')
        socials = BloggerSocialMedia.objects.filter(blogger=blogger).all()
        context.update({
            'socials': socials,
            'title': post.title,
            'comments': comments,
            'post': post,
            'similar_posts': similar_posts,
            'blogger': blogger,
            'popular_posts': Post.objects.filter(post_verify="ACTIVE").order_by('-hit_count_generic__hits')[:3],
        })
        return context

class PrevPostDetailView(HitCountDetailView):
    model = Post
    template_name = 'bnews/singleblog.html'
    context_object_name = 'post'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        post = Post.objects.filter(id=get_prev_id(self.kwargs['post_id'])).first()
        similar_posts = Post.objects.filter(category=post.category, post_verify="ACTIVE").all()
        blogger = Blogger.objects.filter(user_ptr_id=self.request.user.id).first()
        context = super(PrevPostDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(post=post, reply__isnull=True).order_by('-created_at')
        socials = BloggerSocialMedia.objects.filter(blogger=blogger).all()
        context.update({
            'socials': socials,
            'title': post.title,
            'comments': comments,
            'post': post,
            'similar_posts': similar_posts,
            'blogger': blogger,
            'popular_posts': Post.objects.filter(post_verify="ACTIVE").order_by('-hit_count_generic__hits')[:3],
        })
        return context






@csrf_exempt
def blogs(request):
    if request.method == 'POST':
        typesearch = request.POST.get('typesearch')
        if typesearch == "category":
            c = request.POST.get('category')
            if int(c) == 0:
                posts = Post.objects.filter(post_verify="ACTIVE").order_by('-created_at')
                categories = Category.objects.all()
                context = {
                    'c': 0,
                    'title': 'Blogs',
                    'posts': posts,
                    'categories': categories,
                    'count': Post.objects.filter(post_verify="ACTIVE").order_by('-created_at')
                }
                return render(request, 'bnews/blogs.html', context)
            else:
                cat = Category.objects.filter(id=int(c)).first()
                posts = Post.objects.filter(category=cat,post_verify="ACTIVE").order_by('-created_at');
                categories = Category.objects.all()
                context = {
                    'c':cat.id,
                    'title': cat.category + ' Blogs',
                    'posts': posts,
                    'categories': categories,
                    'count': Post.objects.filter(post_verify="ACTIVE").order_by('-created_at')
                }
                return render(request, 'bnews/blogs.html', context)
        elif typesearch == "search":
            search = request.POST.get('search')
            posts = Post.objects.filter(
                Q(category__category__icontains=search) |
                Q(title__icontains=search) |
                # Q(title__) or
                Q(description__icontains=search) |
                Q(slug__icontains=search) |
                Q(blogger__first_name__icontains=search) |
                Q(blogger__last_name__icontains=search) |
                Q(blogger__biography__icontains=search) |
                Q(blogger__county__county__icontains=search)
            ).filter(post_verify="ACTIVE").order_by('-created_at')
            categories = Category.objects.all()
            context = {
                'title': 'Blogs',
                'posts': posts,
                'search_item':search,
                'categories': categories,
                'count': Post.objects.filter(post_verify="ACTIVE").order_by('-created_at')
            }
            return render(request, 'bnews/blogs.html', context)
    else:
        posts = Post.objects.filter(post_verify="ACTIVE").order_by('-created_at')
        categories = Category.objects.all()
        context = {
            'c': 0,
            'title': 'Blogs',
            'posts': posts,
            'categories': categories,
            'count': Post.objects.filter(post_verify="ACTIVE").order_by('-created_at')
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
                        sweetify.success(request, title='Welcome Admin', text='Welcome Back', persistent='Continue',
                                         timer=1500)
                        return redirect('BLOGBACK:home')
                    if user.is_active:
                        if Blogger.objects.filter(user_ptr_id=user.id, group_status='VIEWER',
                                                  is_user_active='ACTIVATE').exists():
                            login(request, user)
                            sweetify.success(request, title='Welcome', text='You successfully Logged in.',
                                             persistent="Ok", timer=1500)
                            return redirect('BLOG:home')
                        elif Blogger.objects.filter(user_ptr_id=user.id, group_status='BLOGGER',
                                                    is_user_active="ACTIVATE").exists():
                            login(request, user)
                            sweetify.success(request, title='Welcome ', text='Welcome Back', persistent='Continue',
                                             timer=1500)
                            return redirect('BLOGBACK:home')
                        else:
                            sweetify.error(request, 'Error', text='Account Suspended. Contact Admin',
                                           persistent='Retry')
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
                        if Blogger.objects.filter(user_ptr_id=user.id, group_status='VIEWER',
                                                  is_user_active='ACTIVATE').exists():
                            login(request, user)
                            sweetify.success(request, title='Welcome', text='You successfully Logged in.',
                                             persistent='Continue', timer=1500)
                            return redirect('BLOG:home')
                        elif Blogger.objects.filter(user_ptr_id=user.id, group_status='BLOGGER',
                                                    is_user_active='ACTIVATE').exists():
                            login(request, user)
                            sweetify.success(request, title='Welcome ', text='Welcome Back',
                                             persistent='Continue',
                                             timer=1500)
                            return redirect('BLOGBACK:home')
                        else:
                            sweetify.error(request, 'Error', text='Account Suspended. Contact Admin',
                                           persistent='Retry')
                            return redirect(request.META['HTTP_REFERER'])
                else:
                    sweetify.error(request, 'Error', text='Invalid Email and Password', persistent='Retry')
                    return redirect(request.META['HTTP_REFERER'])
        else:
            sweetify.error(request, 'Error', text='Invalid Credentials dont exist', persistent='Retry')
            return redirect(request.META['HTTP_REFERER'])
    return redirect(request.META['HTTP_REFERER'])

@csrf_exempt
def likePost(request , post_id):
    blogger = Blogger.objects.filter(user_ptr_id=request.user.id).first()
    if request.method == 'POST':
        idd = request.POST.get('id')
        post =Post.objects.filter(id=int(idd)).first()
        if not PostLike.objects.filter(post=post, blogger=blogger).first():
            PostLike.objects.create(
                post=post,
                blogger=blogger
            )
            post_cnt = PostLike.objects.filter(post=post).count()
            context={
                'status':'liked',
                'count': post_cnt,
            }
        elif PostLike.objects.filter(post=post, blogger=blogger).first():
            postlike = PostLike.objects.filter(post=post, blogger=blogger).first()
            post_cnt = PostLike.objects.filter(post=post).count()
            if postlike:
                postlike.delete()
                context = {
                    'status': 'unliked',
                    'count': post_cnt,
                }



    return JsonResponse(context)


def comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.filter(id=int(post_id)).first()
        blogger = Blogger.objects.filter(user_ptr_id=request.user.id).first()
        if post:
            msg_content = request.POST.get('msg_content')
            Comment.objects.create(
                msg_content=msg_content,
                blogger=blogger,
                post=post,
            )

            # sweetify.success(request, 'Success', text='', persistent='Ok')
        else:
            sweetify.success(request, 'Error', text='Post Not Found', persistent='Try Again')


    return redirect(request.META['HTTP_REFERER'])


def replycomment(request, post_id, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.filter(id=comment_id).first()
        post = Post.objects.filter(id=int(post_id)).first()
        blogger = Blogger.objects.filter(user_ptr_id=request.user.id).first()
        if comment:
            msg_content = request.POST.get('msg_content')
            Comment.objects.create(
                msg_content=msg_content,
                blogger=blogger,
                post=post,
                reply=comment,
            )

            # sweetify.success(request, 'Success', text='', persistent='Ok')
        else:
            sweetify.success(request, 'Error', text='Post Not Found', persistent='Try Again')

    return redirect(request.META['HTTP_REFERER'])


def userAccount(request):
    blogger = Blogger.objects.filter(user_ptr_id=request.user.id).first()
    if blogger:
        name = 'userAccount'
        if blogger.first_name is not None and blogger.last_name is not None:
            name = blogger.first_name+' '+blogger.last_name

        context = {
            'title': name,
            'counties': County.objects.all(),
            'blogger': blogger,
            'socials': BloggerSocialMedia.objects.filter(blogger=blogger).all()
        }
        return render(request, 'bnews/useraccount.html', context)
    return  redirect('BLOG:home')



def change_password(request):
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


def addsocial(request):
    if request.method == 'POST':
        form = BloggerSocialForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Success', text='Social added', persistent='Ok')
        else:

            sweetify.error(request, 'Error', text='Error add social' , persistent='Ok')

    return redirect(request.META['HTTP_REFERER'])


def updatesocial(request, social_id):
    social = BloggerSocialMedia.objects.filter(id=social_id).first()
    if request.method == "POST":
        form = BloggerSocialForm(request.POST, instance=social)
        if form.is_valid():
            form.save()
            sweetify.success(request, "Success", text="Social updated", persistent='Ok')
        else:
            sweetify.error(request, "Error", text="Error updating social", persistent='Ok')
    return redirect(request.META["HTTP_REFERER"])

def deletesocial(request, social_id):
    social = BloggerSocialMedia.objects.filter(id=social_id).first()
    if social:
        social.delete()
        sweetify.success(request, "Success", text="Social deleted", persistent='Ok')
    else:
        sweetify.error(request, "Error", text="Error deleted social", persistent='Ok')


    return redirect(request.META["HTTP_REFERER"])


def subscribenewsletter(request):
    if request.method == 'POST':
        email  = request.POST.get('email')
        print(email)
        if email:
            if not Newsletter.objects.filter(email=email).exists():
                Newsletter.objects.create(
                    email=email
                )
                sweetify.success(request, "Success", text="Thanks For Subscribing", persistent='Ok')
            else:
                sweetify.error(request, "Error", text="Email exists", persistent='Ok')
        else:
            sweetify.error(request, "Error", text="Error Subscribing", persistent='Ok')
    else:
        sweetify.error(request, "Error", text="Error Subscribing", persistent='Ok')

    return redirect(request.META["HTTP_REFERER"])


# def password_reset_request(request):
#     if request.method == "POST":
#         password_reset_form = PasswordResetForm(request.POST)
#         if password_reset_form.is_valid():
#             data = password_reset_form.cleaned_data['email']
#             associated_users = User.objects.filter(Q(email=data))
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject = "Password Reset Requested"
#                     email_template_name = "bnews/auth/password_reset_email.txt"
#                     c = {
#                     "email":user.email,
#                     'domain':'127.0.0.1:8000',
#                     'site_name': 'Website',
#                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                     "user": user,
#                     'token': default_token_generator.make_token(user),
#                     'protocol': 'http',
#                     }
#                     email = render_to_string(email_template_name, c)
#                     try:
#                         send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
#                     except BadHeaderError:
#                         return HttpResponse('Invalid header found.')
#                     sweetify.success(request, title="Success", text="A message with reset password instructions has been sent to your inbox.", persistent='Ok')
#                     return redirect ("BLOG:password_reset_done")
#     password_reset_form = PasswordResetForm()
#     return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})