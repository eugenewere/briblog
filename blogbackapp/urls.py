from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'BLOGBACK'
urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.category, name='category'),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('editcategory/<int:category_id>', views.editcategory, name='editcategory'),
    path('deletecategory/<int:category_id>', views.deletecategory, name='deletecategory'),

    path('posts/', views.posts, name='posts'),
    path('addposts/', views.addposts, name='addposts'),
    path('post_delete/<int:post_id>', views.post_delete, name='post_delete'),
    path('editpost/<int:post_id>', views.edit_post, name='edit_post'),


    path('bloggers/', views.bloggers, name='bloggers'),
    path('bloggers_group_status/<int:blogger_id>', views.bloggers_group_status, name='bloggers_group_status'),
    path('bloggers_active_status/<int:blogger_id>', views.bloggers_active_status, name='bloggers_active_status'),
    path('bloggers_delete/<int:blogger_id>', views.bloggers_delete, name='bloggers_delete'),



    path('edit_status/', views.edit_post_status, name='edit_post_status'),
    path('edutorial_pick/', views.edutorial_pick, name='edutorial_pick'),
    path('add_edutorial_pick/', views.add_edutorial_pick, name='add_edutorial_pick'),
    path('contactusread/', views.contactusread, name='contactusread'),

    path('comments/', views.comments, name='comments'),
    path('social/', views.social, name='social'),

    path('addsocial', views.addsocial, name='addsocial'),
    path('updatesocial/<int:social_id>', views.updatesocial, name='updatesocial'),
    path('deletesocial/<int:social_id>', views.deletesocial, name='deletesocial'),

    path('userAccount/', views.userAccount, name='userAccount'),
    path('updateuserdetails/', views.updateuserdetails, name='updateuserdetails'),
    path('updatemainuserdetails/', views.updatemainuserdetails, name='updatemainuserdetails'),

    path('changepassword/', views.changepassword, name='changepassword'),

    path('newsletter/', views.newsletter, name='newsletter'),
    path('sendemail/', views.sendemail, name='sendemail'),
    path('del_newsletter/<int:news_id>', views.del_newsletter, name='del_newsletter'),

    path('contact/', views.contact, name='contact'),


]
