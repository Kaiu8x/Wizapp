# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out


from .models import User,Category,Story,Comment, Event
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
    context = {
        'stories': stories
    }
    return render(request, 'app/home.html', context)

#Home page seeing only certain category stories
@login_required
def filteredHome(request, categoryId, categoryName):
    stories = Story.objects.filter(category = categoryId).order_by('-ranking')
    context = {
        'stories': stories,
        'category' : Category.objects.get(pk=categoryId)
    }
    return render(request, 'app/home.html', context)

#Categories Page
@login_required
def categories(request):
    context = {'categories': Category.objects.all().order_by('name')}
    return render(request, 'app/categories.html', context)

#Events page
@login_required
def events(request):
    context = {'events': Event.objects.all()}
    return render(request, 'app/eventos.html', context)

#Adult profiles page
@login_required
def profileCreator(request):
    context = {}
    return render(request, 'app/profileCreator.html', context)

#Normal user profiles page
@login_required
def profileNonCreator(request):
    context = {}
    return render(request, 'app/profileNonCreator.html', context)

#Show specific Story
@login_required
def story(request, storyId):
    context = {'story': Story.objects.get(pk=storyId)}
    return render(request, 'app/story.html', context)

#Page for Creating new Stories
@login_required
def submitStory(request):
    form = StoryForm(request.POST or None)
    context = {
        'form': form,
        'stories': Story.objects.all().order_by('-ranking')
    }
    if form.is_valid():#Validates form and Prevents DATABASE INJECTION
        story = form.save(commit=False)
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        category = form.cleaned_data['category']
        story.title = title
        story.message = message
        story.category = category
        story.save()
        return HttpResponseRedirect(reverse('app:home'))

    return render(request, 'app/createStory.html', context)

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
        user.save()
        userProfile = formComplete.save(commit=False)
        birthdate = formComplete.cleaned_data['birthdate']
        bio = formComplete.cleaned_data['biography']
        userProfile.birthdate = birthdate
        userProfile.biograpy = bio
        userProfile.user = user
        userProfile.save()
        messages.success(request, 'Usuario Creado exitosamente')
        return HttpResponseRedirect(reverse('app:userLogin'))

    return render(request, 'app/createUserAccount.html', context)
