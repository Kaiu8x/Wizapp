from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# Create your views here.


def login(request):
    context = {}
    return render(request, 'app/loginIndex.html', context)
