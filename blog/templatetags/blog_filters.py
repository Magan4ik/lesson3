from django import template
from django.contrib.auth import get_user_model
from accounts.models import Follow
from blog.models import Comment

User = get_user_model()

register = template.Library()

@register.filter
def liked_by(comment: Comment, user: User) -> bool:
    return comment.is_liked_by(user=user)

@register.filter
def disliked_by(comment: Comment, user: User) -> bool:
    return comment.is_disliked_by(user=user)

@register.filter
def follow_to(follower: User, user: User) -> bool:
    return Follow.objects.filter(author=follower, user=user).exists()

@register.filter
def is_double(num: int) -> bool:
    return num % 2 == 0
