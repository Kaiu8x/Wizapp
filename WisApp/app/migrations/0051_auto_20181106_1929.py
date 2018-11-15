# Generated by Django 2.1.2 on 2018-11-07 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_comment_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.UserWithProfile', verbose_name='autor del comentario'),
        ),
    ]
