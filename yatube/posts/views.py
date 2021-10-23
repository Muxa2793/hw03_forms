from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render


from .forms import PostForm
from .models import Group, Post, User


# @login_required
def index(request):
    """Main page"""
    template = 'posts/index.html'

    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, template, context)


# @login_required
def group_posts(request, slug):
    """Page with posts sorted by selected group"""
    template = 'posts/group_list.html'

    group = get_object_or_404(Group, slug=slug)
    paginator = Paginator(group.groups.all(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }

    return render(request, template, context)


def profile(request, username):
    """Page with all posts by selected author"""
    template = 'posts/profile.html'

    user_db = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_db)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_count = paginator.count

    context = {
        'page_obj': page_obj,
        'posts_count': posts_count,
        'user_db': user_db,
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
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            author = request.user
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            Post.objects.create(author=author, text=text, group=group)
            return redirect(f'/profile/{author}/')

    form = PostForm()

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'

    post = Post.objects.get(pk=post_id)
    author = request.user
    if post.author != author:
        return redirect(f'/posts/{post_id}')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.save()
            return redirect(f'/posts/{post_id}')

    form = PostForm(instance=post)

    context = {
        'form': form,
        'is_edit': True
    }

    return render(request, template, context)
