from django.db import models
from colorfield.fields import ColorField
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class UserWithProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name='usuario')
    id = models.AutoField(primary_key=True,verbose_name='id')
    birthdate = models.DateField() #Determines if user has adult privileges
    biography = models.CharField(max_length=500, blank=True,verbose_name='biografía')
    followedUsers = models.ManyToManyField("UserWithProfile", blank=True,verbose_name='usuario que sigue')
    followedCategories = models.ManyToManyField("Category", blank=True,verbose_name='Categorías que sigue')
    favoriteStories = models.ManyToManyField("Story",blank=True,verbose_name='historias favoritas',related_name="FavoriteStories")
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


class Category(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    isEvent = models.BooleanField(blank=True,null=True,verbose_name="¿Es un evento?")
    name = models.CharField(max_length=200,verbose_name='nombre')
    description = models.CharField(max_length=10000,verbose_name='descripción')
    color = ColorField(default='#FF0000',verbose_name='color')
    class Meta:
        verbose_name = 'Categoría o Evento'
        verbose_name_plural = 'Categorías o Eventos'
    def __str__(self):
        return self.name

'''class Event(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    name = models.CharField(max_length=200,verbose_name='nombre')
    description = models.CharField(max_length=10000,verbose_name='descripción')
    dateOfEvent = models.DateField(blank=True,verbose_name='fecha del evento')
    color = ColorField(default='#FF0000', verbose_name='color')
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
    def __str__(self):
        return self.name'''


class Story(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    title = models.CharField(max_length=300,verbose_name='título')
    message = models.CharField(max_length=10000,verbose_name='descripción')
    ranking = models.IntegerField(default=0,verbose_name='ranking(número de "me gusta")')
    author = models.ForeignKey(UserWithProfile,on_delete=models.CASCADE, default=None,verbose_name='autor')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='categoría')
    #event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True, blank=True,verbose_name='evento(si pertenece a un evento)')
    image = models.ImageField(upload_to = 'pic_folder/', default = None,blank=True, null = True)
    class Meta:
        verbose_name = 'Historia'
        verbose_name_plural = 'Historias'
    def get_absolute_url(self):
        return reverse('app:home',kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    ranking = models.IntegerField(default=0,verbose_name='ranking(número de "me gusta")')
    message = models.CharField(max_length=10000,verbose_name='descripción del comentario')
    story = models.ForeignKey(Story, on_delete=models.CASCADE,verbose_name='historia a la que pertenece')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None,verbose_name='autor del comentario')
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
    def __str__(self):
        return 'Comment %s for Story %s' %(self.id, self.story)



