from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'BLOG'
urlpatterns = [
    path('',views.home,name='home'),
    path('timeline',views.timeline,name='timeline'),
    path('contact',views.contact,name='contact'),
    path('register',views.register,name='register'),
    path('makeregister',views.makeregister,name='makeregister'),
    path('loginuser',views.loginuser,name='loginuser'),
    path('singleblog',views.singleblog,name='singleblog'),
    path('blogs',views.blogs,name='blogs'),
    path('logout',views.logout_user,name='logout'),
]