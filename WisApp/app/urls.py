
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings


app_name = "app"

urlpatterns = [
    path('returnPage/', views.returnPage, name='returnPage'),
    path('crearCuenta', views.submitNewUser, name="createNewAccount"),
    path('modificarInfoPerfil<pk>', views.UserWithProfileUpdate.as_view(), name="UserWithProfileUpdate"),
    path('login/', views.login, name='userLogin'),
    path('inicio/', views.home, name='home'),
    path('inicio/Categoria-<categoryId>-<categoryName>/', views.filteredHome, name='filteredHome'),
    path('inicio/MisHistorias/', views.homeMyStories, name='homeMyStories'),
    path('inicio/MisHistorias/Favoritas', views.homeMyFavoriteStories, name='homeMyFavoriteStories'),
    path('inicio/autoresSeguidos/', views.followedAuthors, name='followedAuthors'),
    path('categorias/', views.categories, name='categories'),
    path('eventos/', views.events, name='events'),
    path('ver/perfil/<userId>', views.profile, name='profile'),
    path('historia/<storyId>', views.story, name='story'),
    path('crearHistoria/', views.submitStory, name='createStory'),
    path('modificarHistoria<pk>/', views.StoryUpdate.as_view(), name='storyUpdate'),
    path('eliminarHistoria<pk>/', views.StoryDelete.as_view(), name='storyDelete'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

]