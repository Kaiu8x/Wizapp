# Generated by Django 2.1.2 on 2018-11-07 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_remove_comment_ranking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='story',
        ),
        migrations.AddField(
            model_name='story',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='StoryComments', to='app.Comment', verbose_name='Comentarios en la historia'),
        ),
    ]
