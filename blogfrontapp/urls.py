from django.conf.urls import url
from . import views
from django.urls import path

from .views import PostDetailView, NextPostDetailView, PrevPostDetailView
from django.contrib.auth import views as auth_views  # import this

app_name = 'BLOG'
urlpatterns = (
    path('', views.home, name='home'),
    path('timeline', views.timeline, name='timeline'),
    path('contact', views.contact, name='contact'),
    path('addcontact', views.addcontact, name='addcontact'),
    path('register', views.register, name='register'),
    path('makeregister', views.makeregister, name='makeregister'),
    path('updateuserdetails', views.updateuserdetails, name='updateuserdetails'),
    path('loginuser', views.loginuser, name='loginuser'),
    path('nextsingleblog/<str:slug>/<int:post_id>', NextPostDetailView.as_view(), name='nextsingleblog'),
    path('previoussingleblog/<str:slug>/<int:post_id>', PrevPostDetailView.as_view(), name='previoussingleblog'),
    path('singleblog/<str:slug>/<int:post_id>/', PostDetailView.as_view(), name='singleblog'),
    path('likepost/<int:post_id>', views.likePost, name='likepost'),
    path('comment/<int:post_id>', views.comment, name='comment'),
    path('replycomment/<int:post_id>/<int:comment_id>', views.replycomment, name='replycomment'),
    path('blogs', views.blogs, name='blogs'),
    path('logout', views.logout_user, name='logout'),
    path('userAccount', views.userAccount, name='userAccount'),
    path('change_password', views.change_password, name='change_password'),
    path('addsocial', views.addsocial, name='addsocial'),
    path('updatesocial/<int:social_id>', views.updatesocial, name='updatesocial'),
    path('deletesocial/<int:social_id>', views.deletesocial, name='deletesocial'),
    path('subscribenewsletter/', views.subscribenewsletter, name='subscribenewsletter'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),











    # path('password_reset/done/', auth_views.PasswordResetDoneView, name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
    # path("password_reset/", auth_views.PasswordResetForm, name="password_reset")
)
