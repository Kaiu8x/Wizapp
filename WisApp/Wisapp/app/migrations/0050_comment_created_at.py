# Generated by Django 2.1.2 on 2018-11-07 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_auto_20181106_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Creación'),
        ),
    ]
