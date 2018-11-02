from django.db import models
from colorfield.fields import ColorField
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.


class UserWithProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    birthdate = models.DateField() #Determines if user has adult privileges
    biography = models.CharField(max_length=500, blank=True)
    followedUsers = models.ManyToManyField("UserWithProfile", blank=True)
    favoriteStories = models.ManyToManyField("Story",blank=True)
    #profileImage = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')

    def __str__(self):
        return self.user.__str__()


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    color = ColorField(default='#FF0000')
    def __str__(self):
        return self.name

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    dateOfEvent = models.DateField(blank=True)
    def __str__(self):
        return self.name


class Story(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    message = models.CharField(max_length=10000)
    ranking = models.IntegerField(default=0)
    author = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE, default=3, blank=True)
    #image = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')

    def get_absolute_url(self):
        return reverse('app:home',kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    ranking = models.IntegerField(default=0)
    message = models.CharField(max_length=10000)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return 'Comment %s for Story %s' %(self.id, self.story)



