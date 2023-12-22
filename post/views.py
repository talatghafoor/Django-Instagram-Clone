from django.shortcuts import render, redirect, get_object_or_404
from post.models import Post, Tag, Follow, Stream, Likes
from django.contrib.auth.decorators import login_required
from post.forms import NewPostform
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from accounts.models import Profile
from comment.models import Comment
from comment.forms import NewCommentForm
# Create your views here.

def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context ={
        'post_items' : post_items
    }
    return render(request, 'index.html', context)


def NewPost(request):
    user = request.user
    # profile = get_object_or_404(Profile, user=user)
    tags_obj = []
    
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            P, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            P.tags.set(tags_obj)
            P.save()
            return redirect('index')
    else:
        form = NewPostform()
    context = {
        'form': form
    }
    return render(request, 'newpost.html', context)


def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-details', args=[post.id]))
    else:
        form = NewCommentForm()

    context = {
        'post' : post,
        'form' :form,
        'comments':comments,
    }

    return render(request, 'postdetail.html', context)

    

def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    context = {
        'posts': posts,
        'tag': tag

    }
    return render(request, 'tag.html', context)

@transaction.atomic
def Like(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).exists()
    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes += 1
    else:
        # Delete the existing like entry
        Likes.objects.filter(user=user, post=post).delete()
        current_likes -= 1
    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('post-details', args=[post_id]))


def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))
    









        

