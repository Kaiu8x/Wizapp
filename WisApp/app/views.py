# Create your views here.
from django.shortcuts import render
from .models import User,Category,Story,Comment, Event
from .forms import *
def login(request):
    context = {}
    return render(request, 'app/loginIndex.html', context)

def home(request):
    stories = Story.objects.all().order_by('-ranking')
    context = {
        'stories': stories
    }
    return render(request, 'app/home.html', context)

def categories(request):
    context = {}
    return render(request, 'app/categories.html', context)

def events(request):
    context = {}
    return render(request, 'app/eventos.html', context)

#Adult profiles
def profileCreator(request):
    context = {}
    return render(request, 'app/profileCreator.html', context)

#Normal user profiles
def profileNonCreator(request):
    context = {}
    return render(request, 'app/profileNonCreator.html', context)

def story(request):
    context = {}
    return render(request, 'app/story_form.html', context)

#Page for Creating new Stories
def submitStory(request):
    form = StoryForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        form.save()
        return render(request, 'app/createStory.html', context)

    return render(request, 'app/createStory.html', context)

