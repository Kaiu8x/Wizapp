# Generated by Django 2.1.2 on 2018-11-02 23:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_userwithprofile_favoritestories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwithprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuario'),
        ),
    ]
