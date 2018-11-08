# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse,reverse_lazy
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Q

from .models import Category,Story,Comment
from .forms import *

#login page
def login(request):
    form = UserLoginForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        print('*************')
        print(request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('app:home')
        else:
            messages.error(request, 'Usuario o contraseña incorrecta')
    return render(request, 'app/loginIndex.html', context)

@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Gracias por visitar Wisapp')
#Home page
@login_required
def home(request):
    stories = Story.objects.all().order_by('-created_at')
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    query = request.GET.get("q")
    extraData = None
    if query:
         stories = Story.objects.filter(Q(title__icontains=query)|Q(author__user__username__icontains=query)).order_by('-ranking')
         extraData = 'Search'
    if request.POST:
        if 'favStory' in request.POST:
            favorite = request.POST.get('favStory')
            if request.POST.get('favStory'):
                if favorite == 'favorite':
                    userProfile.favoriteStories.add(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:home'))
                else:
                    userProfile.favoriteStories.remove(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:home'))
        if 'likeStory' in request.POST:
            favorite = request.POST.get('likeStory')
            if request.POST.get('likeStory'):
                if favorite == 'like':
                    userProfile.likedStories.add(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking + 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:home'))
                else:
                    userProfile.likedStories.remove(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking - 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:home'))
    context = {
        'stories': stories,
        'userProfile' : userProfile,
        'extraData': extraData
    }
    return render(request, 'app/home.html', context)

def search(request):
    stories = Story.objects.all().order_by('-created_at')
    query = request.GET.get("q")
    if query:
        stories = Story.objects.filter(Q(title__icontains=query) | Q(author__user__username__icontains=query)).order_by(
            '-ranking')
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    if request.POST:
        if 'favStory' in request.POST:
            favorite = request.POST.get('favStory')
            if request.POST.get('favStory'):
                if favorite == 'favorite':
                    userProfile.favoriteStories.add(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:home'))
                else:
                    userProfile.favoriteStories.remove(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:home'))
        if 'likeStory' in request.POST:
            favorite = request.POST.get('likeStory')
            if request.POST.get('likeStory'):
                if favorite == 'like':
                    userProfile.likedStories.add(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking + 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:home'))
                else:
                    userProfile.likedStories.remove(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking - 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:home'))
    context = {
        'stories': stories,
        'userProfile': userProfile
    }
    return HttpResponseRedirect(reverse('app:home'))

#Home page seeing only certain category stories
@login_required
def filteredHome(request, categoryId, categoryName):
    stories = Story.objects.filter(category = categoryId).order_by('-created_at')
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    if request.POST:
        if 'favStory' in request.POST:
            favorite = request.POST.get('favStory')
            if request.POST.get('favStory'):
                if favorite == 'favorite':
                    userProfile.favoriteStories.add(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:home'))
                else:
                    userProfile.favoriteStories.remove(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:home'))
        if 'likeStory' in request.POST:
            favorite = request.POST.get('likeStory')
            if request.POST.get('likeStory'):
                if favorite == 'like':
                    userProfile.likedStories.add(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking + 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:home'))
                else:
                    userProfile.likedStories.remove(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking - 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:home'))
    context = {
        'stories': stories,
        'category' : Category.objects.get(pk=categoryId),
        'userProfile' : userProfile
    }
    return render(request, 'app/home.html', context)

@login_required
def homeMyStories(request):
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    if request.POST:
        if 'favStory' in request.POST:
            favorite = request.POST.get('favStory')
            if request.POST.get('favStory'):
                if favorite == 'favorite':
                    userProfile.favoriteStories.add(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:homeMyStories'))
                else:
                    userProfile.favoriteStories.remove(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:homeMyStories'))
        if 'likeStory' in request.POST:
            favorite = request.POST.get('likeStory')
            if request.POST.get('likeStory'):
                if favorite == 'like':
                    userProfile.likedStories.add(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking + 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:homeMyStories'))
                else:
                    userProfile.likedStories.remove(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking - 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:homeMyStories'))
    stories = Story.objects.filter(author = userProfile.id).order_by('-created_at')
    context = {
        'stories': stories,
        'userProfile': userProfile
    }
    return render(request, 'app/home.html', context)

@login_required
def homeMyFavoriteStories(request):
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    stories = userProfile.favoriteStories.all()
    if request.POST:
        if 'favStory' in request.POST:
            favorite = request.POST.get('favStory')
            if request.POST.get('favStory'):
                if favorite == 'favorite':
                    userProfile.favoriteStories.add(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:homeMyFavoriteStories'))
                else:
                    userProfile.favoriteStories.remove(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:homeMyFavoriteStories'))
        if 'likeStory' in request.POST:
            favorite = request.POST.get('likeStory')
            if request.POST.get('likeStory'):
                if favorite == 'like':
                    userProfile.likedStories.add(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking + 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:homeMyFavoriteStories'))
                else:
                    userProfile.likedStories.remove(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking - 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:homeMyFavoriteStories'))
    context = {
        'stories': stories,
        'userProfile': userProfile,
        'favoriteStories': 'favorite'
    }
    return render(request, 'app/home.html', context)

@login_required
def storyFilterByAuthor(request, pk):
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    stories = Story.objects.filter(author = pk).order_by('title')
    if request.POST:
        if 'favStory' in request.POST:
            favorite = request.POST.get('favStory')
            if request.POST.get('favStory'):
                if favorite == 'favorite':
                    userProfile.favoriteStories.add(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:homeMyFavoriteStories'))
                else:
                    userProfile.favoriteStories.remove(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:homeMyFavoriteStories'))
        if 'likeStory' in request.POST:
            favorite = request.POST.get('likeStory')
            if request.POST.get('likeStory'):
                if favorite == 'like':
                    userProfile.likedStories.add(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking + 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:homeMyFavoriteStories'))
                else:
                    userProfile.likedStories.remove(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking - 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:homeMyFavoriteStories'))
    context = {
        'stories': stories,
        'userProfile': userProfile,
    }
    return render(request, 'app/home.html', context)

@login_required
def followedAuthors(request):
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    followed = userProfile.followedUsers.all()
    context = {
        'followedUsers': followed,
        'userProfile': userProfile,
    }
    return render(request, 'app/followedUsers.html', context)


#Categories Page
@login_required
def categories(request):
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    if request.POST:
        if 'followCategory' in request.POST:
            follow = request.POST.get('followCategory')
            if follow == 'follow':
                userProfile.followedCategories.add(request.POST.get('categoryId'))
                return HttpResponseRedirect(reverse('app:categories'))
            else:
                userProfile.followedCategories.remove(request.POST.get('categoryId'))
                return HttpResponseRedirect(reverse('app:categories'))
    if userProfile.followedCategories.all().filter():
        userIsFollowed = True
    context = {
        'categories': Category.objects.filter(Q(isEvent=False) | Q(isEvent = None)).order_by('name'),
        'userProfile': userProfile
    }
    return render(request, 'app/categories.html', context)

#Events page
@login_required
def events(request):
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    context = {
        'events': Category.objects.filter(isEvent=True).order_by('-name'),
        'userProfile': userProfile}
    return render(request, 'app/eventos.html', context)

#User profile page
@login_required
def profile(request, userId):
    user = UserWithProfile.objects.get(user = userId)
    userProfile = UserWithProfile.objects.get(user = request.user.id)
    if request.POST:
        if 'followUserProfile' in request.POST:
            follow = request.POST.get('followUserProfile')
            if follow == 'follow':
                userProfile.followedUsers.add(request.POST.get('userProfileId'))
                return HttpResponseRedirect(reverse('app:profile', kwargs={'userId': userId}))
            else:
                userProfile.followedUsers.remove(request.POST.get('userProfileId'))
                return HttpResponseRedirect(reverse('app:profile', kwargs={'userId': userId}))

    userIsFollowed = False
    if userProfile.followedUsers.all().filter(pk = user.id):
        userIsFollowed = True

    context = {
        'currentUser': request.user,
        'userProfile': user,
        'isAdult': user.isAdult(),
        'userIsFollowed': userIsFollowed
    }
    return render(request, 'app/viewProfile.html', context)

#Show specific Story
@login_required
def story(request, storyId):
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    story = Story.objects.get(pk=storyId)
    form = CommentForm(request.POST or None)
    comments = story.comments.all().order_by('created_at')
    if request.POST:
        if 'favStory' in request.POST:
            favorite = request.POST.get('favStory')
            if request.POST.get('favStory'):
                if favorite == 'favorite':
                    userProfile.favoriteStories.add(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:story', kwargs={'storyId':story.id}))
                else:
                    userProfile.favoriteStories.remove(request.POST.get('storyId'))
                    return HttpResponseRedirect(reverse('app:story', kwargs={'storyId':story.id}))
        if 'likeStory' in request.POST:
            favorite = request.POST.get('likeStory')
            if request.POST.get('likeStory'):
                if favorite == 'like':
                    userProfile.likedStories.add(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking + 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:story', kwargs={'storyId':story.id}))
                else:
                    userProfile.likedStories.remove(request.POST.get('storyId'))
                    storyLiked = Story.objects.get(pk=request.POST.get('storyId'))
                    storyLiked.ranking = storyLiked.ranking - 1
                    storyLiked.save()
                    return HttpResponseRedirect(reverse('app:story', kwargs={'storyId':story.id}))
        if 'eraseComment' in request.POST:
            favorite = request.POST.get('eraseComment')
            if request.POST.get('eraseComment'):
                if favorite == 'erase':
                    comment = Comment.objects.get(pk = request.POST.get('commentId'))
                    comment.delete()
                    return HttpResponseRedirect(reverse('app:story', kwargs={'storyId': story.id}))

    context = {'story': story,
               'userProfile': userProfile,
               'comments': comments,
               'form': form
               }
    if form.is_valid():#Validates form and Prevents DATABASE INJECTION
        comment = form.save(commit=False)
        message = form.cleaned_data['message']
        author = userProfile
        comment.message = message
        comment.author = author
        comment.save()
        story.comments.add(comment)
        story.save()
        return HttpResponseRedirect(reverse('app:story', kwargs={'storyId':story.id}))
    return render(request, 'app/story.html', context)

#Page for Creating new Stories
@login_required
def submitStory(request):
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    form = StoryForm(request.POST or None)
    context = {
        'form': form,
        'stories': Story.objects.all().order_by('-ranking'),
        'userProfile': userProfile
    }
    if form.is_valid():#Validates form and Prevents DATABASE INJECTION
        story = form.save(commit=False)
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        category = form.cleaned_data['category']
        currentlyLoggedUser = request.user
        userProfile = UserWithProfile.objects.get(user = currentlyLoggedUser.id)
        story.author = userProfile
        story.title = title
        story.message = message
        story.category = category
        if 'image' in request.FILES:
            story.image = request.FILES['image']
        story.save()
        userProfile.writtenStories.add(story)
        return HttpResponseRedirect(reverse('app:home'))

    return render(request, 'app/createStory.html', context)

class StoryUpdate(UpdateView):
    model = Story
    form_class = StoryForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('app:home')

class StoryDelete(DeleteView):
    model = Story
    success_url = reverse_lazy('app:home')

#Page for Creating new user accounts
def submitNewUser(request):
    form = UserForm(request.POST or None)
    formComplete = UserProfileForm(request.POST or None)
    context = {
        'form': form,
        'formComplete': formComplete
    }
    if form.is_valid() and formComplete.is_valid():#Validates form and Prevents DATABASE INJECTION
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        username = username.lower()
        password = form.cleaned_data['password']
        user.username = username
        user.set_password(password)
        userProfile = formComplete.save(commit=False)
        birthdate = formComplete.cleaned_data['birthdate']
        bio = formComplete.cleaned_data['biography']
        if 'profileImage' in request.FILES:
            uploadedImage = request.FILES['profileImage']
            userProfile.profileImage = uploadedImage
        userProfile.birthdate = birthdate
        userProfile.biograpy = bio
        user.save()
        userProfile.user = user
        userProfile.save()
        messages.success(request, 'Usuario Creado exitosamente')
        return HttpResponseRedirect(reverse('app:userLogin'))

    return render(request, 'app/createUserAccount.html', context)

class UserWithProfileUpdate(UpdateView):
    model = UserWithProfile
    form_class = UserProfileForm
    template_name_suffix = '_update_form'
    def get_success_url(self):
        pk = self.kwargs['pk']
        profileId = UserWithProfile.objects.get(pk = pk)
        return reverse_lazy('app:profile', kwargs={'userId': profileId.user.id})

@login_required
def returnPage(request):
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))