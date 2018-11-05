# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse,reverse_lazy
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out
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
    stories = Story.objects.all().order_by('-ranking')
    query = request.GET.get("q")
    if query:
         stories = Story.objects.filter(Q(title__icontains=query)|Q(author__user__username__icontains=query)).order_by('-ranking')
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    context = {
        'stories': stories,
        'userProfile' : userProfile
    }
    return render(request, 'app/home.html', context)

#Home page seeing only certain category stories
@login_required
def filteredHome(request, categoryId, categoryName):
    stories = Story.objects.filter(category = categoryId).order_by('-ranking')
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
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
    stories = Story.objects.filter(author = userProfile.id).order_by('-ranking')
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
    context = {
        'stories': stories,
        'userProfile': userProfile,
        'favoriteStories': 'favorite'
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
        follow = request.POST.get('followCategory')
        if follow == 'follow':
            userProfile.followedCategories.add(request.POST.get('categoryId'))
            return HttpResponseRedirect(reverse('app:categories'))
        else:
            userProfile.followedCategories.remove(request.POST.get('categoryId'))
            return HttpResponseRedirect(reverse('app:categories'))

    context = {
        'categories': Category.objects.filter(Q(isEvent=False) | Q(isEvent = None)).order_by('-name'),
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
    isAdult = False
    user = UserWithProfile.objects.get(user = userId )
    context = {
        'currentUser': request.user,
        'userProfile': user,
        'isAdult': user.isAdult()
    }
    return render(request, 'app/viewProfile.html', context)

#Show specific Story
@login_required
def story(request, storyId):
    currentlyLoggedUser = request.user
    userProfile = UserWithProfile.objects.get(user=currentlyLoggedUser.id)
    context = {'story': Story.objects.get(pk=storyId), 'userProfile': userProfile}
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
        uploadedImage = request.FILES['image']
        currentlyLoggedUser = request.user
        userProfile = UserWithProfile.objects.get(user = currentlyLoggedUser.id)
        story.author = userProfile
        story.title = title
        story.message = message
        story.category = category
        story.image = uploadedImage
        story.save()
        userProfile.writtenStories.add(story)
        return HttpResponseRedirect(reverse('app:home'))

    return render(request, 'app/createStory.html', context)

#@login_required
class StoryUpdate(UpdateView):
    model = Story
    form_class = StoryForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('app:home')

#@login_required
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
        password = form.cleaned_data['password']
        user.username = username
        user.set_password(password)
        userProfile = formComplete.save(commit=False)
        birthdate = formComplete.cleaned_data['birthdate']
        bio = formComplete.cleaned_data['biography']
        uploadedImage = request.FILES['profileImage']
        userProfile.birthdate = birthdate
        userProfile.biograpy = bio
        user.save()
        userProfile.user = user
        userProfile.profileImage = uploadedImage
        userProfile.save()
        messages.success(request, 'Usuario Creado exitosamente')
        return HttpResponseRedirect(reverse('app:userLogin'))

    return render(request, 'app/createUserAccount.html', context)

class UserWithProfileUpdate(UpdateView):
    model = UserWithProfile
    form_class = UserProfileForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('app:home')

@login_required
def returnPage(request):
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))