from django import template

from ..models import UserWithProfile

register = template.Library()


@register.filter(is_safe=True)
def followed_category(user, pk):
    return UserWithProfile.categoryIsFollowed(user, pk)

@register.filter(is_safe=True)
def favorited_Story(user, pk):
    return UserWithProfile.storyIsFavorited(user, pk)

@register.filter(is_safe=True)
def liked_Story(user, pk):
    return UserWithProfile.storyIsLiked(user, pk)
