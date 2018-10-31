from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# Create your views here.


def login(request):
    context = {}
    return render(request, 'app/loginIndex.html', context)

def home(request):
    context = {}
    return render(request, 'app/home.html', context)

def categories(request):
    context = {}
    return render(request, 'app/categories.html', context)

def events(request):
    context = {}
    return render(request, 'app/eventos.html', context)

def profileCreator(request):
    context = {}
    return render(request, 'app/profileCreator.html', context)

def profileNonCreator(request):
    context = {}
    return render(request, 'app/profileNonCreator.html', context)

def story(request):
    context = {}
    return render(request, 'app/story.html', context)