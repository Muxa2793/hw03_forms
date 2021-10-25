from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from utils.paginator import create_paginator

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    """Main page"""
    template = 'posts/index.html'

    posts = Post.objects.all()
    page_obj = create_paginator(request, posts)

    context = {
        'page_obj': page_obj,
    }

    return render(request, template, context)


def group_posts(request, slug):
    """Page with posts sorted by selected group"""
    template = 'posts/group_list.html'

    group = get_object_or_404(Group, slug=slug)
    page_obj = create_paginator(request, group.groups.all())

    context = {
        'group': group,
        'page_obj': page_obj,
    }

    return render(request, template, context)


def profile(request, username):
    """Page with all posts by selected author"""
    template = 'posts/profile.html'

    user_db = get_object_or_404(User, username=username)
    posts = user_db.posts.all()
    posts_count = posts.count

    page_obj = create_paginator(request, posts)

    context = {
        'posts_count': posts_count,
        'user_db': user_db,
        'page_obj': page_obj,
    }

    return render(request, template, context)


def post_detail(request, post_id):
    """Page showing detail of selected post"""
    template = 'posts/post_detail.html'

    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post
    }

    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'

    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = username = request.user
        post.save()
        return redirect('posts:profile', username=username)

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'

    post = get_object_or_404(Post, pk=post_id)
    username = request.user

    if post.author != username:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)

    context = {
        'form': form,
        'is_edit': True
    }

    return render(request, template, context)
