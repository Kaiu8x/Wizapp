from django.db import models
from colorfield.fields import ColorField
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
from django.utils import timezone


class UserWithProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name='usuario')
    id = models.AutoField(primary_key=True,verbose_name='id')
    birthdate = models.DateField() #Determines if user has adult privileges
    biography = models.CharField(max_length=500, blank=True,verbose_name='biografía')
    followedUsers = models.ManyToManyField("UserWithProfile", blank=True,verbose_name='usuario que sigue')
    followedCategories = models.ManyToManyField("Category", blank=True,verbose_name='Categorías que sigue')
    favoriteStories = models.ManyToManyField("Story",blank=True,verbose_name='historias favoritas',related_name="FavoriteStories")
    likedStories = models.ManyToManyField("Story",blank=True,verbose_name='historias que me gustaron',related_name="LikedStories")
    writtenStories = models.ManyToManyField("Story", blank=True, verbose_name="Historias escritas", related_name="WrittenStories")
    profileImage = models.ImageField(upload_to = 'userpic_folder/', default = None, blank=True, null= True)
    class Meta:
        verbose_name = 'Usuario(Perfil)'
        verbose_name_plural = 'Usuarios(Perfil)'
    def __str__(self):
        return self.user.__str__()
    def isAdult(self):
        return date.today().year - self.birthdate.year > 55
    def getWrittenStories(self):
        return self.writtenStories
    def categoryIsFollowed(self,categoryId):
        if self.followedCategories.all().filter(pk=categoryId):
            return True
        return False
    def storyIsFavorited(self,storyId):
        if self.favoriteStories.all().filter(pk=storyId):
            return True
        return False
    def storyIsLiked(self,storyId):
        if self.likedStories.all().filter(pk=storyId):
            return True
        return False

class Category(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    isEvent = models.BooleanField(blank=True,null=True,verbose_name="¿Es un evento?")
    name = models.CharField(max_length=200,verbose_name='nombre')
    description = models.CharField(max_length=10000,verbose_name='descripción')
    color = ColorField(default='#FF0000',verbose_name='color')
    class Meta:
        verbose_name = 'Categoría o Evento'
        verbose_name_plural = 'Categorías o Eventos'
        ordering = ['name']
    def __str__(self):
        return self.name

class Story(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    title = models.CharField(max_length=300,verbose_name='título')
    message = models.CharField(max_length=10000,verbose_name='descripción')
    ranking = models.PositiveIntegerField(default=0,verbose_name='ranking(número de "me gusta")')
    author = models.ForeignKey(UserWithProfile,on_delete=models.CASCADE, default=None,verbose_name='autor')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='categoría')
    image = models.ImageField(upload_to = 'pic_folder/', default = None,blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Fecha de Creación", blank=True)
    comments = models.ManyToManyField("Comment", blank=True, verbose_name="Comentarios en la historia", related_name="StoryComments")
    class Meta:
        verbose_name = 'Historia'
        verbose_name_plural = 'Historias'
    def get_absolute_url(self):
        return reverse('app:home',kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    message = models.CharField(max_length=10000,verbose_name='descripción del comentario')
    author = models.ForeignKey(UserWithProfile, on_delete=models.CASCADE, default=None,verbose_name='autor del comentario')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Fecha de Creación", blank=True)
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
    def __str__(self):
        return 'Comentario %s %s' %(self.id,self.message[:25])



