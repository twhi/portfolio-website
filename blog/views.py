from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm


def blog_index(request):
    posts = Post.objects.all().order_by('-created_on') # hyphen tells django to order by the largest first
    context = {
        'posts': posts,
        'blog_page': 'active',
    }
    return render(request, 'blog_index.html', context)


def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by('-created_on')
    context = {
        'category': category,
        'posts': posts,
        'blog_page': 'active',
    }
    return render(request, 'blog_category.html', context)


def blog_detail(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)

    # load comment form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data['author'],
                body=form.cleaned_data['body'],
                post=post
            )
            comment.save()
            return HttpResponseRedirect('')
    else:
        form = CommentForm()

    comments = Comment.objects.filter(post=post).order_by('-created_on')
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'blog_page': 'active',
    }
    return render(request, 'blog_detail.html', context)
