from django import template

from blogbackapp.models import *

register = template.Library()


@register.filter("to_url")
def to_url(value):
    return value.replace(" ", "_")


@register.filter("has_he_liked")
def has_he_liked(user_id, post_id):
    blogger = Blogger.objects.filter(user_ptr_id=user_id).first()
    post = Post.objects.filter(id=post_id).first()
    postlike = PostLike.objects.filter(blogger=blogger, post=post).first()
    if postlike:
        return True
    else:
        return False


@register.filter("all_replied_comments")
def all_replied_comments(comment_id):
    print(comment_id, Post.objects.all()[0:1])
    comment = Comment.objects.filter(id=comment_id).first()
    # print()
    print(comment)
    return comment
    # comments = Comment.objects.filter(reply=comment).all()
    # print(post,comments,post, post_id, comment_id)
    # print(post, post_id, comment_id)
    # if comments:
    #     return comments
    # else:
    #     return False


@register.filter("recent_comments")
def recent_comments(request):
    comments = Comment.objects.all().order_by('-created_at')[0:15]
    return comments


@register.filter("footercategories")
def footercategories(request):
    list_category = []
    posts = Post.objects.annotate(itemcount=Count('id')).order_by('-itemcount')
    for c in posts:
        list_category.append(c.category)

    return list(set(list_category))

@register.filter("getbloggerComments")
def getbloggerComments(request):
    blogger=Blogger.objects.filter(user_ptr_id=request.user.id).first()
    return Comment.objects.filter(blogger=blogger).order_by('-created_at')


@register.filter("getAdminComments")
def getAdminComments(request):
    return Comment.objects.order_by('-created_at')