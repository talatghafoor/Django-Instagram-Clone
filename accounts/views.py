from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login


from post.models import Post, Follow, Stream
from django.contrib.auth.models import User
from accounts.models import Profile
# from .forms import EditProfileForm, UserRegisterForm
from django.urls import resolve
# from comment.models import Comment

# Create your views here.

def UserProfile(request, username):
    user = Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    # posts = Post.objects.filter(user=user).order_by('-posted')
    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()
    
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    #paginator
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context ={
        'posts': posts,
        'posts_paginator' : posts_paginator,
        'profile':profile,
        'posts_count': posts_count,
        'following_count': following_count,
        'follow_status': follow_status,
    }

    return render(request, 'profile.html', context)
