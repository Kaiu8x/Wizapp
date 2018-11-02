
from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('crearCuenta', views.submitNewUser, name="createNewAccount"),
    #path('completarPerfil', views.completeUserProfile, name="completeUserProfile"),
    path('login/', views.login, name='userLogin'),
    path('inicio/', views.home, name='home'),
    path('inicio/Categoria-<categoryId>-<categoryName>/', views.filteredHome, name='filteredHome'),
    path('categorias/', views.categories, name='categories'),
    path('eventos/', views.events, name='events'),
    path('perfil/', views.profileCreator, name='profile'),
    #path('perfil-personal/', views.profileNonCreator, name='profile'),
    path('historia/<storyId>', views.story, name='story'),
    path('crearHistoria/', views.submitStory, name='createStory'),
]