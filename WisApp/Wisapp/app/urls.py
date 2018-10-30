
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='userLogin'),
    path('home/', views.home, name='home'),

]