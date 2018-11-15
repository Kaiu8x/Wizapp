from django.contrib.auth.decorators import login_required
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
    path('estadisticas/', views.showStatistics, name='showStatistics'),
    path('inicio/Categoria-<categoryId>-<categoryName>/', views.filteredHome, name='filteredHome'),
    path('inicio/MisHistorias/', views.homeMyStories, name='homeMyStories'),
    path('inicio/MisHistorias/Favoritas', views.homeMyFavoriteStories, name='homeMyFavoriteStories'),
    path('inicio/HistoriasPorAutor/<pk>', views.storyFilterByAuthor, name='storyFilterByAuthor'),
    path('inicio/autoresSeguidos/', views.followedAuthors, name='followedAuthors'),
    path('inicio/search/', views.search, name='search'),
    path('categorias/', views.categories, name='categories'),
    path('eventos/', views.events, name='events'),
    path('ver/perfil/<userId>', views.profile, name='profile'),
    path('historia/<storyId>', views.story, name='story'),
    path('crearHistoria/', views.submitStory, name='createStory'),
    path('crearPeticion/', views.createPetition, name='createPetition'),
    path('modificarHistoria<pk>/', login_required(views.StoryUpdate.as_view()), name='storyUpdate'),
    path('eliminarHistoria<pk>/', views.StoryDelete.as_view(), name='storyDelete'),
    path('eliminarCuenta<pk>/', views.UserDelete.as_view(), name='userwithprofileDelete'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

]