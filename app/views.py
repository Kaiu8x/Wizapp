# Create your views here.
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category,Story,Comment, Event
from .forms import *
#login page
def login(request):
    context = {}
    return render(request, 'app/loginIndex.html', context)

#Home page
def home(request):
    stories = Story.objects.all().order_by('-ranking')
    context = {
        'stories': stories
    }
    return render(request, 'app/home.html', context)

#Home page seeing only certain category stories
def filteredHome(request, categoryId, categoryName):
    stories = Story.objects.filter(category = categoryId).order_by('-ranking')
    context = {
        'stories': stories,
        'category' : Category.objects.get(pk=categoryId)
    }
    return render(request, 'app/home.html', context)

#Categories Page
def categories(request):
    context = {'categories': Category.objects.all().order_by('name')}
    return render(request, 'app/categories.html', context)

#Events page
def events(request):
    context = {'events': Event.objects.all()}
    return render(request, 'app/eventos.html', context)

#Adult profiles page
def profileCreator(request):
    context = {}
    return render(request, 'app/profileCreator.html', context)

#Normal user profiles page
def profileNonCreator(request):
    context = {}
    return render(request, 'app/profileNonCreator.html', context)

#Show specific Story
def story(request, storyId):
    context = {'story': Story.objects.get(pk=storyId)}
    return render(request, 'app/story.html', context)

#Page for Creating new Stories
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

