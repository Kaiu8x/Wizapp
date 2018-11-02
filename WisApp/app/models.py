from django.db import models
from colorfield.fields import ColorField
from django.urls import reverse

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=300)
    birthdate = models.DateField() #Determines if user has adult privileges
    biography = models.CharField(max_length=500, blank=True)
    password = models.CharField(max_length= 300)
    followedUsers = models.ManyToManyField("User", blank=True)
    #profileImage = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')

    def __str__(self):
        return self.username

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
    event = models.ForeignKey(Event,on_delete=models.CASCADE, default=1, blank=True)
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
    def __str__(self):
        return 'Comment %s for Story %s' %(self.id, self.story)



