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

    path('bloggers/', views.bloggers, name='bloggers'),
    path('bloggers_group_status/<int:blogger_id>', views.bloggers_group_status, name='bloggers_group_status'),
    path('bloggers_active_status/<int:blogger_id>', views.bloggers_active_status, name='bloggers_active_status'),
    path('bloggers_delete/<int:blogger_id>', views.bloggers_delete, name='bloggers_delete'),
]
