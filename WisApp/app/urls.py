
from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('login/', views.login, name='userLogin'),
    path('inicio/', views.home, name='home'),
    path('categorias/', views.categories, name='categories'),
    path('eventos/', views.events, name='events'),
    path('perfil/', views.profileCreator, name='profile'),
    path('perfil-personal/', views.profileNonCreator, name='profile'),
    path('historia/', views.story, name='story'),
    #path('crearHistoria/', views.createsStory, name='createStory'),
    path('crearHistoria/', views.submitStory, name='submitStory'),
]