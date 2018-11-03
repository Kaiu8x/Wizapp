
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings


app_name = "app"

urlpatterns = [
    path('crearCuenta', views.submitNewUser, name="createNewAccount"),
    path('login/', views.login, name='userLogin'),
    path('inicio/', views.home, name='home'),
    path('inicio/Categoria-<categoryId>-<categoryName>/', views.filteredHome, name='filteredHome'),
    path('categorias/', views.categories, name='categories'),
    path('eventos/', views.events, name='events'),
    path('perfil/', views.profileCreator, name='profile'),
    #path('perfil-personal/', views.profileNonCreator, name='profile'),
    path('historia/<storyId>', views.story, name='story'),
    path('crearHistoria/', views.submitStory, name='createStory'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

]