from django import template

from ..models import UserWithProfile, Category, Story

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

@register.filter(is_safe=True)
def stories_Category(user,pk):
    return Story.storiesInCategory(user,pk)

@register.filter(is_safe=True)
def adultAccounts(user):
    return UserWithProfile.adultsCount(user)

@register.filter(is_safe=True)
def commonUsersCount(user):
    return UserWithProfile.commonUsersCount(user)
@register.filter(is_safe=True)
def mostVotedStory(user):
    return Story.mostVotedStory(user)