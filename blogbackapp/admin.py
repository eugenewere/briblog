from django.contrib import admin

# Register your models here.
from blogbackapp.models import *

admin.site.register(Post) #Done
admin.site.register(Category) #Done
admin.site.register(County) #Done
admin.site.register(Blogger) #Done
admin.site.register(PostTags) #Done
admin.site.register(BloggerSocialMedia)
admin.site.register(MainSocialMedia)
admin.site.register(PostLike) #Done
admin.site.register(Comment) #Done
admin.site.register(EditorsPick)
admin.site.register(Newsletter)
