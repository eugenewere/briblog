from datetime import date

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

# from
from django import forms

from blogbackapp.models import *


class BloggerForm(forms.Form, UserCreationForm):
    class Meta:
        model = Blogger
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password2',
            'password1',
            'profile_image',
            'county',
            'gender',
            'phone_number',
            'date_of_birth',
            'biography',

        ]

    def clean_username(self):
        super(BloggerForm, self).clean()
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        super(BloggerForm, self).clean()
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user has already registered using this email')
        return email

    def clean_password2(self):
        super(BloggerForm, self).clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords must match')
        return password2

    def clean_date_of_birth(self):
        super(BloggerForm, self).clean()
        '''
        Only accept users aged 13 and above
        '''
        userAge = 18
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()
        if (dob.year + userAge, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('Users must be aged 18 years old and above.'.format(userAge))
        return dob


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'description',
            'title',
            'post_image'
        ]


class BloggerFormUpdate(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'profile_image',
            'county',
            'gender',
            'phone_number',
            'date_of_birth',
            'biography',
        ]

    def clean_date_of_birth(self):
        super(BloggerFormUpdate, self).clean()
        '''
        Only accept users aged 13 and above
        '''
        userAge = 18
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()
        if (dob.year + userAge, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('Users must be aged 18 years old and above.'.format(userAge))
        return dob


class BloggerSocialForm(forms.ModelForm):
    class Meta:
        model = BloggerSocialMedia
        fields = [
            'name',
            'icon',
            'blogger'
        ]


class MainSocialMediaForm(forms.ModelForm):
    class Meta:
        model = MainSocialMedia
        fields = [
            'name',
            'icon',
        ]


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsEmployee
        fields = [
            'name',
            'email',
            'phone',
            'message',
            'website',
        ]
