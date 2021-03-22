import random
from html import escape

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator
from django.db import models
from datetime import datetime
import datetime
from io import BytesIO
from PIL import Image
# from wagtail.admin.edit_handlers import FieldPanel, RichTextField
from django.core.files import File
from ckeditor.fields import RichTextField
# from djrichtextfield.models import RichTextField
# # Create your models here.
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from hitcount.models import HitCount


def compress(image):
    im = Image.open(image)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    new_image = File(im_io, name=image.name)
    return new_image


class Category(models.Model):
    category = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.category)

    @property
    def getCategoryPostCount(self):
        post_count = Post.objects.filter(category=self, post_verify='ACTIVE').count()
        return post_count


class County(models.Model):
    county_number = models.IntegerField(null=False, blank=False)
    county = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.county)


class Blogger(get_user_model()):
    profile_image = models.ImageField(max_length=200, upload_to='bloggers-images', null=True, blank=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    GROUP_STATUS = {
        ('BLOGGER', 'Blogger'),
        ('VIEWER', 'Viewer'),
    }
    group_status = models.CharField(choices=GROUP_STATUS, default='VIEWER', max_length=200, null=True, blank=True)
    ACTIVE_STATUS = {
        ('ACTIVATE', 'Activate'),
        ('DEACTIVATE', 'Deactivate'),
    }
    is_user_active = models.CharField(choices=ACTIVE_STATUS, default='ACTIVATE', max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(default=datetime.datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    biography = models.TextField()

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.is_user_active)

    class Meta:
        verbose_name = 'Blogger'
        verbose_name_plural = 'Bloggers'

    def save(self, *args, **kwargs):
        new_image = compress(self.profile_image)
        self.profile_image = new_image
        super().save(*args, **kwargs)

    @property
    def newsletterSubscribed(self):
        nwlter = Newsletter.objects.filter(email=self.email).first()
        # print(nwlter)
        if nwlter:
            return True
        else:
            return False

    @property
    def postcount(self):
        return Post.objects.filter(blogger_id=self.id, post_verify='ACTIVE').count()

    def bloggerSocialMedia(self):
        print(BloggerSocialMedia.objects.filter(blogger_id=self.id).all())
        return BloggerSocialMedia.objects.filter(blogger_id=self.id).all()

def random_string():
    return str(random.randint(1, 9999999))

class Post(models.Model):
    post_image = models.FileField( upload_to='post-images', null=True, blank=True)
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(default='', editable=False, max_length=160)
    POST_VERIFY = {
        ('ACTIVE', 'active'),
        ('INACTIVE', 'inactive'),
    }
    post_verify = models.CharField(choices=POST_VERIFY, default='INACTIVE', max_length=200, null=False, blank=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify((self.title.lower()).replace(" ", "-") +'-'+random_string() )
        super().save(*args, **kwargs)


    @property
    def html_stripped(self):
        from django.utils.html import strip_tags
        return strip_tags(self.description)

    @property
    def getComments(self):
        return Comment.objects.filter(post=self).all().order_by('-created_at')
    @property
    def getPrimaryComments(self):
        return Comment.objects.filter(post=self, reply__isnull=True).all().order_by('-created_at')

    def getSecondaryComments(self):
        c = Comment.objects.filter(reply_id=self.id).order_by('-created_at')
        print(c)
        return c

    @property
    def checkInEdutorial(self):
        e = EditorsPick.objects.filter(post_id=self.id, editor_status='ACTIVE').last()
        if e:
            return True
        else:
            return False

    @property
    def likecount(self):
        post_count=PostLike.objects.filter(post_id=self.id).count()

        return post_count

    @property
    def commentcount(self):
        post_count=Comment.objects.filter(post=self).count()
        return post_count

    def img_save(self, *args, **kwargs):
        new_image = compress(self.post_image)
        self.post_image = new_image
        super().save(*args, **kwargs)

    @property
    def getHitcountOfPost(self):
        hit = HitCount.objects.filter(object_pk=self.id).first()
        if hit:
            return hit.hits
        return  0

    @property
    def post_tag(self):
        # print(PostTags.objects.filter(post=self).all())
        return PostTags.objects.filter(post=self).all()


class PostTags(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.title


class BloggerSocialMedia(models.Model):
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, blank=False)
    icon = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MainSocialMedia(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    icon = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s', self.post.title, self.blogger.first_name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE, null=False, blank=False)
    reply = models.ForeignKey('self', related_name="commentreply", on_delete=models.CASCADE, null=True, blank=True)
    msg_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        template = '{0.post}'
        return template.format(self)

    @property
    def getSecondaryComments(self):
        return Comment.objects.filter(reply_id=self.id).all().order_by('-created_at')


class EditorsPick(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    EDITOR_STATUS = {
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    }
    editor_status = models.CharField(choices=EDITOR_STATUS, default='ACTIVE', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s', self.post.title


class Newsletter(models.Model):
    email = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.email)
