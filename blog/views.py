from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.urls import reverse

from blog import models

User = get_user_model()

# Create your views here.

@require_http_methods(["GET"])
def post_list_view(request: HttpRequest) -> HttpResponse:
    mes = ""
    get_data = request.GET.copy()
    page = get_data.pop("page", False)
    if not page:
        page = 1
    else:
        page = int(page[0])
    list_page = page*2 - 1  # Page for [:]
    if username := request.GET.get("username"):
        user = get_object_or_404(User, username=username)
        posts = models.Post.published.filter(author=user)
        mes = f"Posts by {username}"
    elif date := request.GET.get("date"):
        posts = models.Post.published.filter(publish__date=date)
        mes = f"Posts published on {date}"
    elif category_id := request.GET.get("category"):
        category = get_object_or_404(models.Category, pk=int(category_id))
        posts = models.Post.published.filter(category=category)
        mes = f"Posts in the \"{category.name}\" category"
    elif search := request.GET.get("search"):
        post_list = models.Post.published.all()
        posts = list()
        for post in post_list:
            if search.lower() in post.title.lower() or search.lower() in post.body.lower():
                posts.append(post)
        mes = f"Posts by search \"{search}\""
    else:
        posts = models.Post.published.all()

    filters = '&' + get_data.urlencode()
    posts = posts[(list_page-1):(list_page+1)]
    context = {"posts": posts,
               "mes": mes,
               "page": page,
               "filters": filters}

    return render(request, "blog/post/post_list.html", context)

@login_required
@require_http_methods(["GET", "POST"])
def post_detail_view(request: HttpRequest, slug_name: str) -> HttpResponse:
    post = models.Post.published.filter(slug=slug_name)[0]
    if request.user.is_superuser:
        comments = post.comments.all()
    else:
        comments = post.comments.filter(active=True)

    if request.method == "POST":
        if request.user.is_superuser:
            if comment_id := request.POST.get("active"):
                comment = get_object_or_404(models.Comment, pk=int(comment_id))
                comment.active = not comment.active
                comment.save()
                return HttpResponseRedirect(f"{comment.post.get_absolute_url()}#comment{comment.pk}")
            elif comment_id := request.POST.get("delete"):
                comment = get_object_or_404(models.Comment, pk=int(comment_id))
                comment.delete()
                return HttpResponseRedirect(f"{comment.post.get_absolute_url()}#comment{comment.pk}")

        if request.user.is_authenticated:
            body = request.POST.get("comment", "")
            if len(body) >= 5:
                comment = models.Comment.objects.create(post=post, author=request.user, body=body)
                comment.save()
                return redirect("blog:detail", slug_name=slug_name)
            else:
                messages.error(request, "Minimum length 5 characters")
                return render(request, "blog/post/post_detail.html", {"post": post, "comments": comments})
        else:
            messages.error(request, "You must be logged in")
            return render(request, "blog/post/post_detail.html", {"post": post, "comments": comments})

    return render(request, "blog/post/post_detail.html", {"post": post, "comments": comments})


@login_required
def add_commentlike_view(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment = get_object_or_404(models.Comment, id=comment_id)
    like, created = models.CommentLike.objects.get_or_create(comment=comment, user=request.user)
    if created:
        if comment.is_disliked_by(request.user):
            dislike = comment.dislikes.get(user=request.user)
            dislike.delete()
    else:
        like.delete()
    return HttpResponseRedirect(f"{comment.post.get_absolute_url()}#comment{comment.pk}")

@login_required
def add_commentdislike_view(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment = get_object_or_404(models.Comment, id=comment_id)
    dislike, created = models.CommentDislike.objects.get_or_create(comment=comment, user=request.user)
    if created:
        if comment.is_liked_by(request.user):
            like = comment.likes.get(user=request.user)
            like.delete()
    else:
        dislike.delete()
    return HttpResponseRedirect(f"{comment.post.get_absolute_url()}#comment{comment.pk}")


@login_required
def add_postlike_view(request: HttpRequest, slug_name: str) -> HttpResponse:
    post = get_object_or_404(models.Post, slug=slug_name)
    like, created = models.PostLike.objects.get_or_create(post=post, user=request.user)
    if created:
        if post.is_disliked_by(user=request.user):
            dislike = post.dislikes.get(user=request.user)
            dislike.delete()
    else:
        like.delete()
    return HttpResponseRedirect(f"{post.get_absolute_url()}#postFooter")

@login_required
def add_postdislike_view(request: HttpRequest, slug_name: str) -> HttpResponse:
    post = get_object_or_404(models.Post, slug=slug_name)
    dislike, created = models.PostDislike.objects.get_or_create(post=post, user=request.user)
    if created:
        if post.is_liked_by(user=request.user):
            like = post.likes.get(user=request.user)
            like.delete()
    else:
        dislike.delete()
    return HttpResponseRedirect(f"{post.get_absolute_url()}#postFooter")
