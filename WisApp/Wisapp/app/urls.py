
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='userLogin'),
    path('inicio/', views.home, name='home'),
    path('categorias/', views.categories, name='categories'),
    path('eventos/', views.events, name='events'),
    path('perfil/', views.profileCreator, name='profile'),
    path('perfil-personal/', views.profileNonCreator, name='profile'),
    path('historia/', views.story, name='story'),
]